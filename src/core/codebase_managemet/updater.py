import os.path
import shutil
import zipfile

import requests

from core.codebase_managemet.version import VersionManager
from core.config import API_URL, RESOURCE_FOLDER

class Updater:
    def scan(self):
        libs = self.scan_lib()
        self.scan_web()

        for lib in libs.keys():
            if libs[lib]["outdated"]:
                print(f"Updating {lib}...")
                self.download_lib(lib, libs[lib])

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
                if server_version is None or version_core_tuple >= tuple(server_version):
                    print(f"The Lib {lib} is up to date")
                else:
                    print(f"The Lib {lib} is outdated")
                update[lib] = {
                    "outdated": server_version is None or version_core_tuple < tuple(server_version),
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

        r = server_version["name"] is None or not version.check_version_tuple(tuple(server_version["version"]))
        if r:
            print("Alex is up to date")
        else:
            print("Alex is out dated")

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

            with open(os.path.join(target_folder, ".version"), "x") as version_file:
                version_file.write(".".join(list(map(lambda x: str(x), lib_data["new"]))))

    def download_core(self):
        raise NotImplementedError
