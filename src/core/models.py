import uuid

from core.config import EventPriority
from core.intents.slots import *

class ReminderObject:
     id: str
     time: SlotValueInstantTime
     action: SlotValue
     person: SlotValue | None

     callback = lambda reminder, late=True: ...

     def __init__(
             self,
             time: SlotValueInstantTime,
             action: SlotValue,
             person: SlotValue | None = None,
             uid: str | None = None,
     ) -> None:
          self.time = time
          self.action = action
          self.person = person

          self.id = str(uuid.uuid4()) if uid is None else uid

     def get_hour_and_minute(self):
          if self.time.get_hour() == "00" and self.time.get_minute() == "00":
               return "12:00"
          else:
               return f"{self.time.get_hour()}:{self.time.get_minute() == '00'}"

     def seconds(self):
          return self.time.diference_from_now_to_value().total_seconds()

     def get_action(self):
          return self.action.value

     def schedule(self, alex):
          seconds = self.seconds()
          if seconds > 0:
               alex.schedule(seconds, EventPriority.SKILLS, self.callback, self)
          else:
               if seconds > (-60) * 60 * 2:
                    self.callback(self, True)

     def save_callback(self, callback):
          self.callback = callback
