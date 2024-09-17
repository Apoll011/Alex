from core.skills import BaseSkill

class Repeat(BaseSkill):
    def init(self):
        self.register("alex@repeat")
        self.can_go_again = False
        self.can_repeat_responce = False

    def execute(self, intent):
        super().execute(intent)

        last_responce = self.alex_context.load("last_responce")

        if last_responce is None:
            self.responce_translated("not.enough.data")
        else:
            self.responce_translated("repeat.text", {"text": last_responce})
