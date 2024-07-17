import json
import uuid
from dataclasses import dataclass
from core.skills import BaseSkill
from core.intents.slots import *
from core.config import EventPriority
from core.resources.data_files import DataFile


class ReminderObject:
     id: str
     time: SlotValueInstantTime
     action: SlotValue
     person: SlotValue | None

     def __init__(self, time: SlotValueInstantTime, action: SlotValue, person: SlotValue | None = None) -> None:
          self.time = time
          self.action = action
          self.person = person

          self.id = str(uuid.uuid4())

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

     def load(self, uuid):
          d = DataFile.get(uuid, "reminder")
          reminder_json = json.loads(d)
          self.id = reminder_json["id"]
          self.time = SlotValueInstantTime(reminder_json["time"]["kind"], reminder_json["time"]["value"], reminder_json["time"]["grain"], reminder_json["time"]["precision"])
          self.action = SlotValue(reminder_json["action"]["kind"], reminder_json["action"]["value"])
          self.person = None
          if reminder_json["person"] != None:
               self.person = SlotValue(reminder_json["person"]["kind"], reminder_json["person"]["value"])

class Reminder(BaseSkill):
     def init(self):
          self.register("set@reminder")
          self.save_responce_for_context = False
          
     def execute(self, context, intent):
          super().execute(context, intent)
          print(intent.json)
          self.require("time", SlotValueInstantTime)
          self.require("action")
          self.optional("person")

          reminder = ReminderObject(self.slots["time"], self.slots["action"]) # type: ignore
          if self.slot_exists("person"):
               reminder = ReminderObject(self.slots["time"], self.slots["action"], self.slots["person"]) # type: ignore

          reminder.save()
          print(reminder.time.to_datetime())
          