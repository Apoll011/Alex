import os
import subprocess

from core.intents.responce import BoolResponce
from core.skills import BaseSkill

class Something(BaseSkill):
    def init(self):
        self.register("close@something")
        self.can_go_again = False

    def execute(self, intent):
        super().execute(intent)
        self.require("entityName")

        try:
            self.run()
        except subprocess.CalledProcessError:
            self.say("not.found", name=self.get("entityName"))

    def run(self):
        c = f"pidof -d \";\" {self.get("entityName")}"
        pids = subprocess.check_output(c, shell=True, text=True)
        self.pids = pids.split(";")
        self.question(
            "confirmation.ask" if len(self.pids) == 1 else "more.than.one", self.confirmation,
            {"name": self.get("entityName")}, BoolResponce()
        )

    def confirmation(self, responce: bool):
        if responce:
            self.kill()
        else:
            self.say("cancel.kill")

    def kill(self):
        for pid in self.pids:
            os.system(f"kill {pid}")
