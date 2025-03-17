from core.skills import BaseSkill

class PresentsMaker(BaseSkill):
    def init(self):
        self.register("alex@presents.maker")

    def execute(self, intent):
        super().execute(intent)
        self.say("who.made.alex", creator=self.get_creator().name)

    def get_creator(self):
        user = self.alex().persons.search_tags("Creator")[0]
        return user
