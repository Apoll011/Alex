import os

from core.skills import BaseSkill

class SearchFor(BaseSkill):
    def init(self):
        self.register("dictionary@search.for")

    def execute(self, intent):
        super().execute(intent)
        self.require("search")

        search_command = f"nohup firefox  --search \"{self.get("search")}\" > /dev/null 2>&1 &"

        os.system(search_command)

        self.say("ok")
