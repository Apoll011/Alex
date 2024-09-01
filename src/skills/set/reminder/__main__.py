import os
import pickle
from core.intents.slots import *
from core.skills import BaseSkill
from core.models import ReminderObject
from core.resources.data_files import DataFile

class Reminder(BaseSkill):
     def init(self):
          self.register("set@reminder")
          self.save_responce_for_context = False
          
     def execute(self, context, intent):
          super().execute(context, intent)
          self.require("time", SlotValueInstantTime)
          self.require("action")
          self.optional("person")

          reminder = ReminderObject(self.slots["time"], self.slots["action"]) # type: ignore
          if self.slot_exists("person"):
               reminder = ReminderObject(
                         self.slots["time"], # type: ignore
                         self.slots["action"], 
                         self.slots["person"]
                    ) 

          reminder.save_callback(self.fire_reminder)
          
          with open(DataFile.getPath(reminder.id, "reminder"), "wb") as f:
               pickle.dump(reminder, f)

          reminder.schedule(self.alex())
          
          if reminder.person == None:
               self.responce_translated("reminder.set", {
                         "time": self.get_raw_slot_value("time"), 
                         "action": reminder.get_action()
                         })
          else:
               self.responce_translated("reminder.set.person", {
                         "time": self.get_raw_slot_value("time"), 
                         "action": reminder.get_action(), 
                         "person": reminder.person.value
                         })
          

     def fire_reminder(self, reminder: ReminderObject, late = False):
          if reminder.person == None:
               self.responce_translated(f"reminder.fire{'.late' if late else ''}", {
                    "action": reminder.get_action()
                    })
          else:
               self.responce_translated(f"reminder.fire.person{'.late' if late else ''}", {
                    "action": reminder.get_action(), 
                    "person": reminder.person.value
                    })
          os.remove(DataFile.getPath(reminder.id, "reminder"))
