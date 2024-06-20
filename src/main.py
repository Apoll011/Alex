from core.nexus.ai import Nexus
from core.system.config import __version__
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

parser.add_argument("-v", "--version", action="version", version=f"Alex {__version__}")

args = parser.parse_args()

if args.train or args.start:
    Nexus.start_nexus()
    if args.train:
        Nexus.request_ai("ALEX", "retrain")
    else:
        Nexus.call_ai("PRIA", "start")
