from core.system.ai.nexus import Nexus
from core.system.version import VersionManager
import argparse
import zipfile
import os

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

parser.add_argument("-i", "--install-skill", action=InstallSkill, nargs=2, help="Install a skill")
parser.add_argument("-t", "--train", action="store_true", help="Train all the resources from Alex and exit")
parser.add_argument("-s", "--start", action="store_true", help="Start Alex")
parser.add_argument("-d", "--debug", action="store_true", help="Enters Debug Mode")
parser.add_argument("-c", "--cmd", action="store_true", help="Enters Comand Line Mode")

parser.add_argument("-v", "--version", action="version", version=f"Alex {VersionManager.get().get("coreVersion", "")}")

args = parser.parse_args()

if args.train or args.start:
    Nexus.start_nexus()

    if args.debug:
        Nexus.request_ai("ALEX", "debugMode")
    if not args.cmd:
        Nexus.request_ai("ALEX", "serverMode")

    if args.train:
        Nexus.request_ai("ALEX", "retrain")

    else:
        Nexus.call_ai("PRIA", "start")
