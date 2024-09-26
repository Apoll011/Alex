from core.skills import BaseSkill

class Something(BaseSkill):
    def init(self):
        self.register("close@something")
        self.can_go_again = False

    def execute(self, intent):
        super().execute(intent)
        self.require("entityName")
