from core.notifier import AlexEvent
from core.skills import BaseSkill
from core.utils import is_morning

class Hi(BaseSkill):
    def init(self):
        self.register("saudation@hi")
        self.can_go_again = False

    def execute(self, intent):
        super().execute(intent)
        self.optional("timeOfDay")

        self.master_name = self.alex_context.load("master").name

        if self.slot_exists("timeOfDay"):
            if is_morning():
                is_morning()
                self.register_event(AlexEvent.ALEX_GOOD_MORNING)
            self.responce_translated("greet.hi.based.on.time.of.day", {"time": self.slots["timeOfDay"]})
        else:
            self.responce_translated("greet.hi", {"user": self.master_name})

    def morning_routine(self):
        if self.alex_context.load("master").is_birth():
            self.responce_translated("happy.birth", {"user": self.master_name})
