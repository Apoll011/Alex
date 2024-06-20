from core.nexus.ai import Nexus
from core.system.config import __version__
import argparse


class InstallSkill(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        file = values


parser = argparse.ArgumentParser()

parser.add_argument("-i", "--install-skill", action=InstallSkill, help="Install a skill")
parser.add_argument("-t", "--train", action="store_true", help="Train all the resources from Alex and exit")
parser.add_argument("-s", "--start", action="store_true", help="Start Alex")

parser.add_argument("-v", "--version", action="version", version=f"Alex {__version__}")

args = parser.parse_args()
print(args)
if args.train or args.start:
    Nexus.start_nexus()
    if args.train:
        Nexus.request_ai("ALEX", "retrain")
    else:
        Nexus.call_ai("PRIA", "start")
