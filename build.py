import os
import shutil
import subprocess

import requests

from src.core.codebase_managemet.version import VersionManager

def build_lib():
    url = "http://0.0.0.0:1178/version_control/lib/last"

    l = ["web", "audio", "language", "model"]
    for lib in l:
        with open(f"./resources/lib/{lib}/.version", "r") as version_file:
            version = version_file.read()
            version_core_tuple = tuple(map(lambda v: int(v), version.split(".")))

        responce = requests.get(url + f"?lib_type={lib}")
        server_version = responce.json()["version"]
        if server_version is None or version_core_tuple > tuple(server_version):
            print(f"Saving {lib} version {version_core_tuple}...")
            os.system(f"zip -r {lib}.zip ./resources/lib/{lib}")
            file = {"file": open(f"{lib}.zip", "rb")}
            responce = requests.post(
                url=f"http://0.0.0.0:1178/version_control/lib/upload?version={'.'.join(map(lambda x: str(x), version_core_tuple))}&lib_type={lib}",
                files=file
            )
            r = responce.json()["responce"]
            if r:
                print(f"Sent {lib} successfully.")
            os.system(f"rm -f {lib}.zip")

def build_alex():
    url = "http://0.0.0.0:1178/version_control/main/last"
    version = VersionManager()

    response = requests.get(url)
    server_version = response.json()

    platforms = {
        "linux": "pyinstaller --add-data './src/skills:skills' --distpath ./dist/linux ./src/main.py",
    }

    if server_version["name"] is None or version.check_version_tuple(tuple(server_version["version"])):
        print(f"Saving Alex version {version.get()['coreVersion']}...")
        for platform in platforms.keys():
            print("Compiling Alex for", platform)

            # Create dist directory if it doesn't exist
            os.makedirs(f"./dist/{platform}", exist_ok=True)

            # Run PyInstaller
            subprocess.run(platforms[platform], shell=True, check=True)

            # Zip the result
            shutil.make_archive(f"alex_{platform}", 'zip', f"./dist/{platform}/main")

            # Upload the zipped file
            with open(f"alex_{platform}.zip", "rb") as file:
                response = requests.post(
                    url=f"http://0.0.0.0:1178/version_control/main/upload?version={'.'.join(map(str, version.get_tuple()))}&platform={platform}",
                    files={"file": file}
                )
            r = response.json()
            if r:
                print(f"Sent {platform} Alex successfully.")

            # Clean up
            os.remove(f"alex_{platform}.zip")
            os.system("rm -r dist")
            os.remove("main.spec")

def built_resources():
    if not os.path.isdir("/home/pegasus/.alex_resources"):
        print("Copying Resources")
        os.system("cp -r ./resources /home/pegasus/.alex_resources")
    else:
        print("Copying Lib...")
        os.system("rm -f -r /home/pegasus/.alex_resources/lib")
        os.system("cp -r ./resources/lib /home/pegasus/.alex_resources/lib")

if __name__ == '__main__':
    build_lib()
    build_alex()
    built_resources()
    print("Build process completed.")
