from core.skills import BaseSkill
from core.config import EventPriority
from core.intents.slots import SlotValueDuration

class Timer(BaseSkill):
     def init(self):
          self.register("set@timer")
          
     def execute(self, context, intent):
          super().execute(context, intent)
          self.require("duration", SlotValueDuration)
          self.optional("entity")

          self.duration: SlotValueDuration = self.slots["duration"] # type: ignore

          self.define()

          self.responce_translated("timer.defined", {"time": self.duration.to_string()})

     def define(self):
          total_seconds = self.duration.get_total_seconds()
          if self.slot_exists("entity"):
               self.alex().schedule(total_seconds, EventPriority.SKILLS, self.fire_timer_with_entity)
          else:
               self.alex().schedule(total_seconds, EventPriority.SKILLS, self.fire_timer)

     def fire_timer(self):
          self.request_atention()
          self.responce_translated("timer.fire")
     
     def fire_timer_with_entity(self):
          self.request_atention()
          self.responce_translated("timer.fire.entity")
