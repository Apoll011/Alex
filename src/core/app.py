import argparse
import os
import sys
import zipfile

from core.alex import ALEX
from core.codebase_managemet.app import home, is_compiled
from core.codebase_managemet.build import Build
from core.codebase_managemet.make import PrepareWorkSpace
from core.codebase_managemet.updater import Updater
from core.codebase_managemet.version import VersionManager
from core.config import config_file
from core.error import ServerClosed
from core.interface import *
from core.interface.api import API
from core.log import LOG

class InstallSkill(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        file = values[0]  # type: ignore
        intent = values[1]  # type: ignore
        print(f"\33[32mStarting Installation of \33[33m{intent}\33[0m")
        s = intent.split("@")
        path = f"{s[0]}/{s[1].replace('.', '_')}/"
        with zipfile.ZipFile(file, "r") as zip_ref:
            zip_ref.extractall("./src/skills/" + path)
            os.system(f"rm -rf./src/skills/{path}/__MACOSX/")
            zip_ref.close()
        print(f"\33[32mEnded Installation of \33[33m{intent}\33[0m")

class ParseArguments:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(epilog="Developed by Tiago Bernardo")

        self.parser.add_argument(
            "--install-skill",
            action=InstallSkill,
            nargs=2,
            help="Install a skill",
            metavar=("file_path", "intent"),
        )
        self.parser.add_argument(
            "-l",
            "--language",
            default="en",
            help="Set the language",
            choices=["en", "pt"],
        )
        self.parser.add_argument(
            "-b",
            "--base-server",
            default=config_file["api"]["host"],
            help="Set the Base Server IP",
            metavar="ip",
        )
        if not is_compiled():
            self.parser.add_argument(
                "--build",
                help="Build Alex and stores him in server. (Only on developer mode)",
                action="store_true"
            )
        self.parser.add_argument(
            "-s", "--start", action="store_true", help="Start Alex"
        )
        self.parser.add_argument(
            "-d", "--debug", action="store_true", help="Enters Debug Mode"
        )
        self.parser.add_argument(
            "--voice", action="store_true", help="Enters voice mode"
        )
        self.parser.add_argument(
            "-i",
            "--interface",
            default="cmd",
            help="Interface mode",
            choices=["cmd", "web", "voice", "api"],
        )
        self.parser.add_argument(
            "-u",
            "--update",
            help="Update Alex to its newest version.",
            action="store_true"
        )

        self.parser.add_argument(
            "--api-host",
            help="Where the api should be hosted (Only on API Interface)",
            default=config_file["api"]["host"],
            metavar="host",
        )
        self.parser.add_argument(
            "--api-port",
            help="Where the api should be hosted (Only on API Interface)",
            default=5927,
            metavar="port"
        )

        self.parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"Alex {VersionManager.get().get('coreVersion', '')}",
        )

    def parse(self):
        arg = self.parser.parse_args()
        if "build" not in arg:
            arg.build = False
        return arg

class InterfaceFactory:
    def __init__(self, args: argparse.Namespace, alex: ALEX) -> None:
        interface_type = args.interface
        match interface_type:
            case "web":
                Server(alex)
            case "voice":
                Voice(alex)
            case "api":
                API(alex, args.api_host, int(args.api_port))
            case "cmd":
                CommandLine(alex)
            case _:
                raise BaseException(f"The interface {interface_type} does not exist.")

        self.interface = BaseInterface.get()

    def get_interface(self):
        return self.interface

    def init_interface(self):
        self.interface.init()

    def start_interface(self):
        self.init_interface()
        LOG.info("Started Alex")
        self.interface.start()

    def close_interface(self):
        print()
        self.interface.close()

class AlexFactory:
    def __init__(self, args) -> None:
        self.args = args
        self.alex = ALEX()

        self.alex.base_server_ip = self.args.base_server

        self.set_language()

    def set_language(self):
        language = self.args.language
        self.alex.set_language(language)

    def activate(self):
        LOG.info("Activating Alex")
        self.alex.activate()
        self.config()

    def config(self):
        if self.args.voice:
            self.alex.handle_request("changeMode", "Voice")
        if self.args.debug:
            self.alex.handle_request("debugMode")

    def deactivate(self):
        self.alex.deactivate()

    def get(self):
        return self.alex

class PID:
    pid_file = f"{home()}/.alex"

    @staticmethod
    def lock():
        pid = os.getpid()
        PID.clean()
        with open(PID.pid_file, "x") as pidfile:
            pidfile.write(str(pid))

    @staticmethod
    def clean():
        os.system(f"rm {PID.pid_file} -f")

class App:
    def __init__(self):
        self.alex = None
        self.interface = None
        parser = ParseArguments()
        self.args = parser.parse()

    def __enter__(self):
        PID.lock()
        PrepareWorkSpace()

        LOG.init()

        return self

    def start(self):
        if self.args.start and not self.args.build and not self.args.update:
            try:
                self.main()
            except KeyboardInterrupt:
                sys.exit(0)
        elif not is_compiled() and self.args.build:
            Build()
        elif self.args.update:
            updater = Updater()

            (alex_up, alex_up_version), libs = updater.scan()

            if alex_up_version > VersionManager.CORE_VERSION_TUPLE:
                print(f"New version ({alex_up_version}) was found updating...")
                updater.update_lib(libs)
                updater.update_alex()
            else:
                print("No new version was found.")

    def main(self):
        try:
            print(self.args)
            input()
            self.init()
        except ServerClosed:
            LOG.info("The Alex Server is closed")
            self.alex.get().screen.clear()
            print("The server is closed")
        except KeyboardInterrupt:
            self.alex.get().screen.clear()
            print("Interrupted the application.")
        except Exception as e:
            LOG.error(f"A critical error occurred {e}.")
        finally:
            self.alex.deactivate()

    def init(self):
        self.alex = AlexFactory(self.args)

        self.interface = InterfaceFactory(self.args, self.alex.get())

        self.alex.activate()
        self.interface.start_interface()

    def __exit__(self, exc_type, exc_val, exc_tb):
        PID.clean()
