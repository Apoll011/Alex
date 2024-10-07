from core.intents.responce import BoolResponce
from core.interface.base import BaseInterface
from core.skills import BaseSkill

class Alex(BaseSkill):
    def init(self):
        self.register("close@alex")
        self.can_go_again = False

    def execute(self, intent):
        super().execute(intent)
        self.question("is.sure", self.after_responce, {}, BoolResponce())

    @staticmethod
    def after_responce(sure):
        if sure:
            BaseInterface.get().close()
