import os
import subprocess

from core.skills import BaseSkill

class App(BaseSkill):
    def init(self):
        self.register("open@app")

    def execute(self, intent):
        super().execute(intent)
        self.require("entityName")

        try:
            name = self.get("entityName")
            if name in self.skill_settings["links"]:
                c = f"nohup open {self.skill_settings["links"][name]} > /dev/null 2>&1 &"
            else:
                subprocess.check_output(f"which {name}", shell=True, text=True)
                c = f"nohup {name} > /dev/null 2>&1 &"
            os.system(c)
            self.say("opening.app", name=name)
        except subprocess.CalledProcessError:
            self.say("not.found", name=self.get("entityName"))
