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
                c = f"nohup open {self.skill_settings["links"][name]} 2>&1"
            else:
                c = f"nohup {name} 2>&1"
            subprocess.run(c, shell=True, text=True, stdin=None, stdout=0)
            self.say("opening.app", name=name)
        except subprocess.CalledProcessError:
            self.say("not.found", name=self.get("entityName"))
