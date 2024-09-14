import argparse
import os
import zipfile

from core.alex import ALEX
from core.interface import *
from core.log import LOG
from core.version import VersionManager

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
            default="127.0.0.1",
            help="Set the Base Server IP",
            metavar="ip",
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
            choices=["cmd", "server", "voice", "api"],
        )

        self.parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"Alex {VersionManager.get().get('coreVersion', '')}",
        )

    def parse(self):
        return self.parser.parse_args()


class InterfaceFactory:
    def __init__(self, interface_type: str, alex: ALEX) -> None:
        match interface_type:
            case "server":
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
        self.alex.base_server_ip = self.args.base_server

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
    pid_file = "/home/pegasus/.alex"

    @staticmethod
    def lock():
        pid = os.getpid()
        PID.clean()
        with open(PID.pid_file, "x") as pidfile:
            pidfile.write(str(pid))

    @staticmethod
    def clean():
        os.system(f"rm {PID.pid_file}")


def main(args):
    LOG.init()

    alex = AlexFactory(args)

    interface = InterfaceFactory(args.interface, alex.get())

    if args.start:
        alex.activate()

        try:
            interface.start_interface()

        except KeyboardInterrupt:
            interface.close_interface()

    alex.deactivate()


if __name__ == "__main__":
    parser = ParseArguments()
    PID.lock()
    main(parser.parse())
    PID.clean()
