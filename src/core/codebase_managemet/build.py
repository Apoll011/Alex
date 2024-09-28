import os
import shutil
import subprocess

import requests

from core.codebase_managemet.version import VersionManager
from core.config import API_URL, LIB_RESOURCE_PATH

class Build:
    def __init__(self):
        print("Started Building")
        self.build_lib()
        self.build_alex()
        print("Build process completed.")

    @staticmethod
    def build_lib():
        url = f"{API_URL}/version_control/lib/last"

        l = ["web", "audio", "language", "model"]
        for lib in l:
            with open(f"{LIB_RESOURCE_PATH}/{lib}/.version", "r") as version_file:
                version = version_file.read()
                version_core_tuple = tuple(map(lambda v: int(v), version.split(".")))

            responce = requests.get(url + f"?lib_type={lib}")
            server_version = responce.json()["version"]
            if server_version is None or version_core_tuple > tuple(server_version):
                print(f"Saving {lib} version {version_core_tuple}...")
                os.system(f"(cd {LIB_RESOURCE_PATH}/{lib} && zip -r ../{lib}.zip .)")
                file = {"file": open(f"{LIB_RESOURCE_PATH}/{lib}.zip", "rb")}
                responce = requests.post(
                    url=f"{API_URL}/version_control/lib/upload?version={'.'.join(map(lambda x: str(x), version_core_tuple))}&lib_type={lib}",
                    files=file
                )
                r = responce.json()["responce"]
                if r:
                    print(f"Sent {lib} successfully.")
                os.system(f"rm -f {LIB_RESOURCE_PATH}/{lib}.zip")

    @staticmethod
    def build_alex():
        url = f"{API_URL}/version_control/main/last"
        version = VersionManager()

        response = requests.get(url)
        server_version = response.json()

        platforms = {
            "linux": "pyinstaller --add-data './src/skills:skills' --collect-all 'main' --add-data './src/skills:src/skills' --distpath ./dist/linux ./src/main.py --onefile",
        }

        if server_version["name"] is None or not version.check_version_tuple(tuple(server_version["version"])):
            print(f"Saving Alex version {version.get()['coreVersion']}...")
            for platform in platforms.keys():
                print("Compiling Alex for", platform)

                # Create dist directory if it doesn't exist
                os.makedirs(f"./dist/{platform}", exist_ok=True)

                # Run PyInstaller
                subprocess.run(platforms[platform], shell=True, check=True)

                # Zip the result
                shutil.make_archive(f"alex_{platform}", 'zip', f"./dist/{platform}")

                # Upload the zipped file
                with open(f"alex_{platform}.zip", "rb") as file:
                    response = requests.post(
                        url=f"{API_URL}/version_control/main/upload?version={'.'.join(map(str, version.get_tuple()))}&platform={platform}",
                        files={"file": file}
                    )
                r = response.json()
                if r:
                    print(f"Sent {platform} Alex successfully.")

                # Clean up
                os.remove(f"alex_{platform}.zip")
                os.system("rm -r dist")
                os.remove("main.spec")