from core.skills import BaseSkill
from core.skills.call import SkillCaller

class Recall(BaseSkill):
    def init(self):
        self.register("alex@recall")
        self.can_go_again = False

    def execute(self, intent):
        super().execute(intent)

        last_intent = self.alex_context.load("last_intent")

        if last_intent is None:
            self.say("not.enough.data")
        else:
            skill = SkillCaller(self.language).call(last_intent)
            skill.execute(last_intent)
