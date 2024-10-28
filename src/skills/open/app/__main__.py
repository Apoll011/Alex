import os
import subprocess

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

        for link in self.skill_settings["links"].keys():
            if name in link.split(","):
                return f"nohup open {self.skill_settings["links"][link]} > /dev/null 2>&1 &", "site"

        for folder in self.skill_settings["folders"].keys():
            if name in folder.split(","):
                return f"nohup open {self.skill_settings["folders"][folder]} > /dev/null 2>&1 &", "folder"

        subprocess.check_output(f"which {name}", shell=True, text=True)
        return f"nohup {name} > /dev/null 2>&1 &", "app"
