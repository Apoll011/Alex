from core.skills import BaseSkill

class Presents(BaseSkill):
    def init(self):
        self.register("alex@presents")

    def execute(self, intent):
        super().execute(intent)
        self.responce_translated("alex.how.he.is", {"user": self.alex_context.load("master")["name"]})  # type: ignore
