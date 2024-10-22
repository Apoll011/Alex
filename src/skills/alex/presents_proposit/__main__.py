from core.skills import BaseSkill

class PresentsProposit(BaseSkill):
    def init(self):
        self.register("alex@presents.proposit")

    def execute(self, intent):
        super().execute(intent)
        self.say("alex.proposit")
