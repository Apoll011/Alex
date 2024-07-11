import os
import zipfile
import argparse
from core.ALEX import ALEX
from core.interface import *
from core.version import VersionManager

class InstallSkill(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        file = values[0] # type: ignore
        intent = values[1] # type: ignore
        print(f"\33[32mStarting Instalation of \33[33m{intent}\33[0m")
        s = intent.split("@")
        path = f"{s[0]}/{s[1].replace(".", "_")}/"
        with zipfile.ZipFile(file, 'r') as zip_ref: # type: ignore
            zip_ref.extractall('./src/skills/'+path)
            os.system(f"rm -rf ./src/skills/{path}/__MACOSX/")
            zip_ref.close()
        print(f"\33[32mEnded Instalation of \33[33m{intent}\33[0m")


parser = argparse.ArgumentParser()

parser.add_argument("-p", "--install-skill", action=InstallSkill, nargs=2, help="Install a skill")
parser.add_argument("-t", "--train", action="store_true", help="Train all the resources from Alex and exit")
parser.add_argument("-s", "--start", help="Start Alex", default="en", choices=["en", "pt"])
parser.add_argument("-d", "--debug", action="store_true", help="Enters Debug Mode")
parser.add_argument("-i", "--interface", help="Interface mode" , default="cmd", choices=["cmd", "server", "voice"])

parser.add_argument("-v", "--version", action="version", version=f"Alex {VersionManager.get().get("coreVersion", "")}")

args = parser.parse_args()

def main(args):
    language = args.start

    alex = ALEX(language)
    alex.activate()

    if args.debug:
        alex.handle_request("debugMode")

    if args.train:
        alex.handle_request("retrain")
    else:
        alex.start()

    if args.interface == "server":
        Server(alex)
    elif args.interface == "voice":
        Voice(alex)
    else:
        ComandLine(alex)

    BaseInterface.get().start()

if __name__ == "__main__":
    main(args)
