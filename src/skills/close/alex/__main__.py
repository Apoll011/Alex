from core.intents.responce import BoolResponce
from core.interface.base import BaseInterface
from core.skills import BaseSkill

class Alex(BaseSkill):
    def init(self):
        self.register("close@alex")
        self.can_go_again = False

    def execute(self, intent):
        super().execute(intent)
        self.question("close.server", self.after_responce, {}, BoolResponce())

    def after_responce(self, close_server):
        if close_server:
            BaseInterface.get().alex.api.call_route("close")
        BaseInterface.get().alex.deactivate()
