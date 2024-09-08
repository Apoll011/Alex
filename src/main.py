import os
import zipfile
import argparse
from core.log import LOG
from core.ALEX import ALEX
from core.interface import *
from core.version import VersionManager

class InstallSkill(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        file = values[0] # type: ignore
        intent = values[1] # type: ignore
        print(f"\33[32mStarting Instalation of \33[33m{intent}\33[0m")
        s = intent.split("@")
        path = f"{s[0]}/{s[1].replace('.', '_')}/"
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall('./src/skills/'+path)
            os.system(f"rm -rf./src/skills/{path}/__MACOSX/")
            zip_ref.close()
        print(f"\33[32mEnded Instalation of \33[33m{intent}\33[0m")


parser = argparse.ArgumentParser(epilog='Developed by Tiago Bernardo')

parser.add_argument("--install-skill", action=InstallSkill, nargs=2, help="Install a skill", metavar=("file_path", "intent"))
parser.add_argument("-t", "--train", action="store_true", help="Train all the resources from Alex and exit")
parser.add_argument("-l", "--language", default="en", help="Set the language", choices=["en", "pt"])
parser.add_argument("-b", "--base-server", default="127.0.0.1", help="Set the Base Server IP", metavar=("ip"))
parser.add_argument("-s", "--start", action="store_true", help="Start Alex")
parser.add_argument("-d", "--debug", action="store_true", help="Enters Debug Mode")
parser.add_argument("--voice", action="store_true", help="Enters voice mode")
parser.add_argument("-i", "--interface", default="cmd", help="Interface mode", choices=["cmd", "server", "voice", "api"])

parser.add_argument("-v", "--version", action="version", version=f"Alex {VersionManager.get().get('coreVersion', '')}")

args = parser.parse_args()

def lock_pid():
    pid = os.getpid()
    clean()
    with open('/home/pegasus/.alex', "x") as pidfile:
        pidfile.write(str(pid))

def clean():
    os.system("rm /home/pegasus/.alex")

def main(args):
    LOG.init()
    language = args.language

    alex = ALEX()

    alex.base_server_ip = args.base_server

    alex.set_language(language)
    LOG.info("Activating alex Alex")
    
    if args.voice:
        alex.handle_request("changeMode", "Voice")
    if args.debug:
        LOG.info("Debug Mode")
        alex.handle_request("debugMode")
    
    if args.interface == "server":
        Server(alex)
    elif args.interface == "voice":
        Voice(alex)
    elif args.interface == "api":
        #API(alex)
        pass
    else:
        ComandLine(alex)
    
    interface = BaseInterface.get()
    
    if args.start:
        alex.activate()

        if args.train:
            LOG.info("Training server")
            alex.handle_request("retrain")
    
        interface.init()

        try:
            LOG.info("Started Alex")
            interface.start()
            
        except KeyboardInterrupt:
            print()
            interface.close()
    
    alex.deactivate()
            
if __name__ == "__main__":
    try:
        lock_pid()
        main(args)
    except Exception:
        pass
    clean()
