from core.skills import BaseSkill
from core.user import User

class PresentsMaker(BaseSkill):
    def init(self):
        self.register("alex@presents.maker")

    def execute(self, intent):
        super().execute(intent)
        self.say("who.made.alex", creator=self.get_creator().name)

    @staticmethod
    def get_creator():
        user = User.search_tags("Creator")[0]
        return user
