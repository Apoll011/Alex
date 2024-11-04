import os
import subprocess

from core.codebase_managemet.app import home
from core.skills import BaseSkill

class App(BaseSkill):
    def init(self):
        self.register("open@app")

    def execute(self, intent):
        super().execute(intent)
        self.require("entityName")

        name = self.get("entityName")
        try:
            self.open(name)
        except subprocess.CalledProcessError:
            self.say("not.found", name=name.title())

    def open(self, name):
        command, open_type = self.get_command(name.lower())
        os.system(command)
        self.say("opening.thing", name=name.title(), type=open_type)

    def get_command(self, name):
        if name == "folder":
            name = self.intent.input.lower().split()[-2]

        links = self.get_links()
        folders = self.get_folders()

        for link in links.keys():
            if name in link.split(","):
                return f"nohup open {links[link]} > /dev/null 2>&1 &", "site"

        for folder in folders.keys():
            if name in folder.split(","):
                return f"nohup open {folders[folder]} > /dev/null 2>&1 &", "folder"

        for app_name in self.setting("apps").keys():
            if name in app_name.split(","):
                name = self.setting("apps")[app_name]
                break

        subprocess.check_output(f"which {name}", shell=True, text=True)
        return f"nohup {name} > /dev/null 2>&1 &", "app"

    def get_links(self):
        links = self.setting("links")
        # TODO: Get links from bookmarks
        return links

    def get_folders(self):
        folders = self.setting("folders")
        for path in os.listdir(home()):
            p = f"{home()}{path}"
            if os.path.isdir(p) and not p.startswith("."):
                if path not in folders:
                    folders[path.lower()] = p

        return folders
