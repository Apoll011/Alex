import json
import uuid
from core.log import LOG
from core.skills import BaseSkill
from core.intents.slots import *
from core.config import EventPriority
from core.resources.data_files import DataFile


class ReminderObject:
     id: str
     time: SlotValueInstantTime
     action: SlotValue
     person: SlotValue | None

     def __init__(self, time: SlotValueInstantTime, action: SlotValue, person: SlotValue | None = None, uid: str | None = None) -> None:
          self.time = time
          self.action = action
          self.person = person

          self.id = str(uuid.uuid4()) if uid == None else uid

     def get_hour_and_minute(self):
          if self.time.get_hour() == "00" and self.time.get_minute() == "00":
               return "12:00"
          else:
               return f"{self.time.get_hour()}:{self.time.get_minute() == "00"}"

     def save(self):
          Reminderjson = {
               "id": self.id,
               "time": {
                    "kind": self.time.kind,
                    "grain": self.time.grain,
                    "precision": self.time.precision,
                    "value": self.time.value
               },
               "action": {
                    "kind": self.action.kind,
                    "value": self.action.value
               },
               "person": None
          }
          if self.person != None:
               Reminderjson["person"] = {
                    "kind": self.person.kind,
                    "value": self.person.value
               }
          with open(DataFile.load(self.id, "reminder"), "w") as remind:
               json.dump(Reminderjson, remind)

     @staticmethod
     def load(uuid):
          d = DataFile.get(uuid, "reminder")
          reminder_json = json.loads(d)
          id = reminder_json["id"]
          time = SlotValueInstantTime(reminder_json["time"]["kind"], reminder_json["time"]["value"], reminder_json["time"]["grain"], reminder_json["time"]["precision"])
          action = SlotValue(reminder_json["action"]["kind"], reminder_json["action"]["value"])
          person = None
          if reminder_json["person"] != None:
               person = SlotValue(reminder_json["person"]["kind"], reminder_json["person"]["value"])
          return ReminderObject(time, action, person, id)
     
     def seconds(self):
          return self.time.diference_from_now_to_value().total_seconds()

     def get_action(self):
          return self.action.value    

     def schedule(self, alex, callback):
          seconds = self.seconds()
          if seconds > 0:
               alex.schedule(seconds, EventPriority.SKILLS, callback, self.id)
          else:
               LOG.debug("removed reminder of id: ", self.id)
               DataFile.delete(self.id, "reminder")

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

          reminder.save()
          
          
          reminder.schedule(self.alex(), self.fire_reminder)
          
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
          

     def fire_reminder(self, id):
          reminder = ReminderObject.load(id)

          if reminder.person == None:
               self.responce_translated("reminder.fire", {
                    "action": reminder.get_action()
                    })
          else:
               self.responce_translated("reminder.fire.person", {
                    "action": reminder.get_action(), 
                    "person": reminder.person.value
                    })
