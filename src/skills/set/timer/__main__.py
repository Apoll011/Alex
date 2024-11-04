from core.config import EventPriority
from core.intents.slots import SlotValueDuration
from core.skills import BaseSkill

class Timer(BaseSkill):
    duration: SlotValueDuration

    def init(self):
        self.register("set@timer")

    def execute(self, intent):
        super().execute(intent)
        self.require("duration", SlotValueDuration)
        self.optional("entity")

        self.duration = self.get_obj("duration")

        self.define()

        self.say("timer.defined", time=self.duration.to_string())

    def define(self):
        total_seconds = self.duration.get_total_seconds()
        if self.slot_exists("entity"):
            self.scheduler().schedule(total_seconds, EventPriority.SKILLS, self.fire_timer_with_entity)
        else:
            self.scheduler().schedule(total_seconds, EventPriority.SKILLS, self.fire_timer)

    def fire_timer(self):
        self.request_attention()
        self.say("timer.fire")

    def fire_timer_with_entity(self):
        self.request_attention()
        self.say("timer.fire.entity", entity=self.get("entity"))
