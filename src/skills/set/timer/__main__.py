from core.skills import BaseSkill
from core.config import EventPriority
from core.intents.slots import SlotValueDuration

class Timer(BaseSkill):
     def init(self):
          self.register("set@timer")
          self.save_responce_for_context = False
          
     def execute(self, context, intent):
          super().execute(context, intent)
          self.require("duration", SlotValueDuration)

          self.duration: SlotValueDuration = self.slots["duration"] # type: ignore

          self.define()

          self.responce_translated("timer.defined", {"time": self.duration.to_string()})

     def define(self):
          self.alex().schedule(self.duration.get_total_seconds(), EventPriority.SKILLS, self.fire_timer)

     def fire_timer(self):
          self.responce_translated("timer.fire")
