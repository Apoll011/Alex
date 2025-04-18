import datetime
import os.path
import shutil
import zipfile
from datetime import timedelta

import requests

from core.ai.ai import AI
from core.codebase_managemet.app import home, restart_app
from core.codebase_managemet.version import VersionManager
from core.config import API_URL, AUTO_UPDATE_SCHEDULED_TIME, EventPriority, RESOURCE_FOLDER, SCHEDULE_TIME
from core.intents.responce import HardBoolResponce
from core.interface import BaseInterface

class Updater:

    def update_lib(self, libs):
        for lib in libs.keys():
            if libs[lib]["outdated"]:
                self.download_lib(lib, libs[lib])

    def update_alex(self):
        self.download_core()

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
        target_folder: str = os.path.join(str(RESOURCE_FOLDER), "lib", lib_type)

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
        self.alex: AI = alex
        self.version_manager = VersionManager
        self.updater = Updater()

    def question(self, text, callback, fallback=None, **kwargs):
        self.up_say(text, fallback, **kwargs)
        self.alex.text_processor.setListenProcessor(callback, HardBoolResponce())

    def up_say(self, key, fallback=None, **kwargs):
        self.alex.speak(self.alex.translate_responce(key, context=kwargs, voice="UPDATER", fallback=fallback))

    def update(self):
        self.up_say("update.start.libraries", fallback="Updating Alex Libraries.")
        self.updater.update_lib(self.libs)
        self.up_say("update.start.alex", fallback="Updating Alex.")
        self.updater.update_alex()
        BaseInterface.get().close()

    def run_update_process(self):
        if not self.is_allowed_to_update():
            return

        (alex_up, alex_up_version), self.libs = self.updater.scan()

        if alex_up_version > self.version_manager.CORE_VERSION_TUPLE:
            self.handle_alex_update(alex_up_version)
        else:
            self.handle_library_updates()

    def handle_alex_update(self, alex_up_version):
        self.question(
            "update.new.alex.version",
            self.handle_alex_update_responce,
            version=VersionManager.versionify(alex_up_version),
            fallback="There is a new Alex version {version} would you like to update it? Be aware that you will need to restart the app."
        )

    def handle_alex_update_responce(self, responce):
        if responce:
            self.update()
        else:
            self.up_say("system.cancel", "Cancelling...")
            self.block_update()

    def handle_library_updates(self):
        try:
            new_libs = [
                (lib, VersionManager.versionify(self.libs[lib]["new"]))
                for lib in self.libs
                if self.libs[lib]["outdated"]
            ]
        except Exception as e:
            print(e)

        if new_libs:
            self.up_say("update.new.libraries", "There are new versions for the Alex libraries.")
            for lib, version in new_libs:
                self.up_say(
                    "update.new.library", name=lib.title(), version=version,
                    fallback="Library {name} version {version}."
                )

            self.question("ask.for.update", self.handle_alex_update_responce, fallback="Would you like to update?")

    def handle_library_updates_responce(self, responce):
        if responce:
            self.up_say("update.start.libraries", "Updating Alex Libraries.")
            self.updater.update_lib(self.libs)
            BaseInterface.get().close()
        else:
            self.up_say("system.cancel", "Cancelling...")
            self.block_update()

    @classmethod
    def block_update(cls):
        cls.allowed_to_update = False

    @classmethod
    def is_allowed_to_update(cls):
        return cls.allowed_to_update

class AutoUpdater:
    def __init__(self):
        self.libs = None
        self.version_manager = VersionManager
        self.updater = Updater()

    def scan(self):
        (alex_up, alex_up_version), self.libs = self.updater.scan()

        if alex_up_version > self.version_manager.CORE_VERSION_TUPLE:
            self.update()

    def update(self):
        self.updater.update_lib(self.libs)
        self.updater.update_alex()
        restart_app()

    @staticmethod
    def seconds_to_scheduled_time():
        now = datetime.datetime.now()
        hour_split = AUTO_UPDATE_SCHEDULED_TIME.split(":")
        target = now.replace(hour=int(hour_split[0]), minute=int(hour_split[1]), second=0, microsecond=0)

        if now >= target:
            target += timedelta(days=1)

        time_difference = target - now
        return int(time_difference.total_seconds())

    def schedule(self, alex: AI):
        alex.scheduler.schedule(self.seconds_to_scheduled_time(), EventPriority.SYSTEM, self.scan_and_schedule, alex)

    def scan_and_schedule(self, alex: AI):
        self.scan()
        alex.scheduler.schedule_recurrent(SCHEDULE_TIME.ONE_DAY, EventPriority.SYSTEM, self.scan)
