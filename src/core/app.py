import argparse
import os
import socket
import sys
import zipfile

import requests

from core.alex import ALEX
from core.codebase_managemet.app import home, is_compiled
from core.codebase_managemet.build import Build
from core.codebase_managemet.make import PrepareWorkSpace
from core.codebase_managemet.version import VersionManager
from core.config import config_file
from core.error import ServerClosed
from core.interface import *
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
    def __init__(self, interface_type: str, alex: ALEX) -> None:
        match interface_type:
            case "web":
                Server(alex)
            case "voice":
                Voice(alex)
            case "api":
                raise NotImplementedError("The api interface is not implemented.")
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

        self.set_base_server()
        self.set_language()

    def set_base_server(self):
        if self.args.base_server == config_file["api"]["host"] and not self.is_base_server(config_file["api"]["host"]):
            self.alex.base_server_ip = self.get_base_server_on_local_net() or self.args.base_server
        else:
            self.alex.base_server_ip = self.args.base_server

    @staticmethod
    def get_base_server_on_local_net():
        local_ip = socket.gethostbyname(socket.gethostname())

        ip_parts = local_ip.split(".")
        base_ip = ".".join(ip_parts[:-1])

        for i in range(1, 255):
            ip = f"{base_ip}.{i}"
            url = f"http://{ip}:{config_file["api"]["port"]}/"

            try:
                responce = requests.get(url, timeout=1)

                if responce.status_code == 200:
                    data = responce.json()
                    if "name" in data and data["name"] == "Alex":
                        return ip
            except (requests.ConnectionError, requests.Timeout):
                pass

        return None

    @staticmethod
    def is_base_server(id):
        try:
            responce = requests.get(f"http://{id}:{config_file["api"]["port"]}/")
            if responce.json()["name"] != "Alex":
                raise KeyError
            return True
        except (KeyError, Exception):
            return False

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
        LOG.init()
        PID.lock()

        PrepareWorkSpace()

        return self

    def start(self):
        if self.args.start and not self.args.build:
            try:
                self.main()
            except KeyboardInterrupt:
                sys.exit(0)
        elif not is_compiled() and self.args.build:
            Build()

    def main(self):
        self.alex = AlexFactory(self.args)

        self.interface = InterfaceFactory(self.args.interface, self.alex.get())

        try:
            self.alex.activate()
            self.interface.start_interface()
        except ServerClosed:
            self.alex.get().screen.clear()
            print("The server is closed")
        except KeyboardInterrupt:
            self.alex.get().screen.clear()
            print("Interrupted the application.")
        finally:
            self.alex.deactivate()

    def __exit__(self, exc_type, exc_val, exc_tb):
        PID.clean()
