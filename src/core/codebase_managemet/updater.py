import os.path
import shutil
import zipfile

import requests

from core.codebase_managemet.app import home
from core.codebase_managemet.version import VersionManager
from core.config import API_URL, RESOURCE_FOLDER
from core.intents.responce import HardBoolResponce
from core.interface import BaseInterface

class Updater:

    def update_lib(self, libs):
        for lib in libs.keys():
            if libs[lib]["outdated"]:
                self.download_lib(lib, libs[lib])

    def update_alex(self):
        self.download_core()
        BaseInterface.get().close()

    def scan(self):
        libs = self.scan_lib()
        alex = self.scan_web()

        return alex, libs

    @staticmethod
    def scan_lib():
        url = f"{API_URL}/version_control/lib/last"

        libs = ["web", "audio", "language", "model"]

        update = {}
        for lib in libs:
            responce = requests.get(url + f"?lib_type={lib}")
            server_version = responce.json()["version"]
            try:
                with open(f"{RESOURCE_FOLDER}/lib/{lib}/.version", "r") as version_file:
                    version = version_file.read()
                    version_core_tuple = tuple(map(lambda v: int(v), version.split(".")))
                update[lib] = {
                    "outdated": server_version is None or version_core_tuple < tuple(server_version or (0, 0, 0)),
                    "current": version_core_tuple, "new": server_version
                }
            except FileNotFoundError:
                update[lib] = {"outdated": True, "current": "None", "new": server_version}

        return update

    @staticmethod
    def scan_web():
        url = f"{API_URL}/version_control/main/last"
        version = VersionManager()

        response = requests.get(url)
        server_version = response.json()

        r = server_version["name"] is not None and version.check_version_tuple(tuple(server_version["version"]))
        return r, tuple(server_version["version"] or (0, 0, 0))

    @staticmethod
    def download_lib(lib_type, lib_data):
        target_folder: str = os.path.join(RESOURCE_FOLDER, "lib", lib_type)

        responce = requests.get(f"{API_URL}/version_control/lib/get?lib_type={lib_type}")

        if responce.status_code == 200:
            zip_file_path = os.path.join(RESOURCE_FOLDER, "lib", f"{lib_type}.zip")

            with open(zip_file_path, "wb") as zip_file:
                zip_file.write(responce.content)

            if os.path.exists(target_folder):
                shutil.rmtree(target_folder)

            os.makedirs(target_folder, exist_ok=True)

            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                zip_ref.extractall(target_folder)

            os.remove(zip_file_path)

    @staticmethod
    def download_core():
        os.system("mkdir /tmp/alex")
        os.system("wget \"http://0.0.0.0:1178/version_control/main/get\" -O /tmp/alex/alex.zip -t 5 -q")
        os.system("unzip -qq /tmp/alex/alex.zip -d /tmp/alex/")
        os.system(f"rm -f {home()}/alex")
        os.system(f"cp /tmp/alex/main {home()}/alex")
        os.system("rm -r /tmp/alex")

class AlexUpdater:
    allowed_to_update = True

    def __init__(self, alex):
        self.libs = None
        self.alex = alex
        self.version_manager = VersionManager
        self.updater = Updater()

    def up_say(self, text):
        self.alex.speak(self.alex.make_responce(text, voice="UPDATER"))

    def update(self):
        self.up_say("Updating Alex Libraries")
        self.updater.update_lib(self.libs)
        self.up_say("Updating Alex")
        self.updater.update_alex()

    @staticmethod
    def check_entry(response):
        if response.startswith("y") or response == "":
            return True
        elif response.startswith("n"):
            return False
        else:
            print(f"Invalid response {response}. Defaulting to yes.")
            return True

    @staticmethod
    def versionify(version):
        return ".".join(map(str, version))

    def run_update_process(self):
        if not self.is_allowed_to_update():
            return

        (alex_up, alex_up_version), self.libs = self.updater.scan()

        if alex_up_version > self.version_manager.CORE_VERSION_TUPLE:
            self.handle_alex_update(alex_up_version)
        else:
            self.handle_library_updates()

    def question(self, text, callback):
        self.up_say(text)
        self.alex.text_processor.setListenProcessor(callback, HardBoolResponce())

    def handle_alex_update(self, alex_up_version):
        self.question(
            f"There is a new Alex version {self.versionify(alex_up_version)} would you like to update it? Be aware that you will need to restart the app.",
            self.handle_alex_update_responce
        )

    def handle_alex_update_responce(self, responce):
        if responce:
            self.update()
            self.alex.deactivate()
        else:
            self.up_say("Canceling...")
            self.block_update()

    def handle_library_updates(self):
        new_libs = [
            (lib, self.versionify(self.libs[lib]["new"]))
            for lib in self.libs
            if self.libs[lib]["outdated"]
        ]

        if new_libs:
            self.up_say("There are new versions for the Alex libraries:")
            for lib, version in new_libs:
                self.up_say(f'Libraries {lib.title()} version {version}')

            self.question("Would you like to update?", self.handle_alex_update_responce)

    def handle_library_updates_responce(self, responce):
        if responce:
            self.up_say("Updating Alex Libraries")
            self.updater.update_lib(self.libs)
            self.alex.deactivate()
        else:
            self.up_say("Canceling...")
            self.block_update()

    @classmethod
    def block_update(cls):
        cls.allowed_to_update = False

    @classmethod
    def is_allowed_to_update(cls):
        return cls.allowed_to_update
