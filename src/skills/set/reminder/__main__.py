import os
import pickle

from core.intents.slots import *
from core.models import ReminderObject
from core.resources.data_files import DataFile
from core.skills import BaseSkill

class Reminder(BaseSkill):
     def init(self):
          self.register("set@reminder")

     def execute(self, intent):
          super().execute(intent)
          self.require("time", SlotValueInstantTime)
          self.require("action")
          self.optional("person")

          reminder = ReminderObject(self.get_obj("time"), self.get_obj("action"))
          if self.slot_exists("person"):
               reminder = ReminderObject(
                   self.get_obj("time"),
                   self.get_obj("action"),
                   self.get_obj("person")
                    ) 

          reminder.save_callback(self.fire_reminder)
          
          with open(DataFile.getPath(reminder.id, "reminder"), "wb") as f:
               pickle.dump(reminder, f)

          reminder.schedule(self.scheduler())

          if reminder.person is None:
              self.say(
                  "reminder.set",
                  time=self.get("time", True),
                  action=reminder.get_action()
              )
          else:
              self.say(
                  "reminder.set.person",
                  time=self.get("time", True),
                  action=reminder.get_action(),
                  person=reminder.person.value
              )
          

     def fire_reminder(self, reminder: ReminderObject, late = False):
         if not late:
             self.request_attention()
         if reminder.person is None:
             self.say(
                 f"reminder.fire{'.late' if late else ''}",
                 action=reminder.get_action()
             )
         else:
             self.say(
                 f"reminder.fire.person{'.late' if late else ''}",
                 action=reminder.get_action(),
                 person=reminder.person.value
                 )
         os.remove(DataFile.getPath(reminder.id, "reminder"))
