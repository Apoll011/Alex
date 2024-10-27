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
        if name.lower() in self.skill_settings["links"]:
            c = f"nohup open {self.skill_settings["links"][name]} > /dev/null 2>&1 &"
        elif name.lower() in self.skill_settings["folders"]:
            c = f"nohup open {self.skill_settings["folders"][name]} > /dev/null 2>&1 &"
        else:
            subprocess.check_output(f"which {name}", shell=True, text=True)
            c = f"nohup {name} > /dev/null 2>&1 &"
        os.system(c)
        self.say("opening.app", name=name.title())
