from core.system.intents import IntentResponse, Slot
from core.nexus.ai import AI
from .error import SkillIntentError, SkillSlotNotFound

class BaseSkill:
     name: str

     is_api: bool = False

     alex: AI
     intent: IntentResponse

     slots: dict[str, Slot | None] = {}

     def __init__(self):
          pass
     
     def set_as_api(self):
          self.is_api = True

     def execute(self, alex: AI, intent: IntentResponse):
          if intent.intent.intent_name != self.name:
               raise SkillIntentError(self.name, intent.intent.intent_name)

          self.alex = alex
          self.intent = intent
               
     def register(self, name):
          self.name = name
     
     def require(self, slot_name: str, slot_type):
          if slot_name in self.intent.slots.keys() and isinstance(self.intent.slots[slot_name].value, slot_type):
               self.slots[slot_name] = self.intent.slots[slot_name].value
          else:
               raise SkillSlotNotFound(slot_name)

     def optional(self, slot_name: str, slot_type):
          if slot_name in self.intent.slots.keys() and isinstance(self.intent.slots[slot_name].value, slot_type):
               self.slots[slot_name] = self.intent.slots[slot_name].value
          else:
               self.slots[slot_name] = None

     def responce(self, text):
          if not self.is_api:
               self.set_as_last_intent(text)
               self.speak(text)
          else:
               return text

     def set_as_last_intent(self, text):
          self.alex.set_context("last_responce", text)
          self.alex.set_context("last_intent", self.intent)

     def speak(self, text):
          print(text)
