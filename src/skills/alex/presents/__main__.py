from core.skills import BaseSkill

class Presents(BaseSkill):
    def init(self):
        self.register("alex@presents")

    def execute(self, intent):
        super().execute(intent)
        self.say("alex.how.he.is", user=self.context_load("master").name)
