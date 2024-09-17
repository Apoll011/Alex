from core.skills import BaseSkill

class Hi(BaseSkill):
    def init(self):
        self.register("saudation@hi")
        self.can_go_again = False

    def execute(self, intent):
        super().execute(intent)
        self.optional("timeOfDay")

        master_name = self.alex_context.load("master")["name"]  # type: ignore

        if self.slot_exists("timeOfDay"):
            self.responce_translated("greet.hi.based.on.time.of.day", {"time": self.slots["timeOfDay"]})
        else:
            self.responce_translated("greet.hi", {"user": master_name})
