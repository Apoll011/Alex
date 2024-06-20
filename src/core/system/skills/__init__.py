from core.system.intents import IntentResponse, Slot
from core.nexus.ai import AI
from .erros import SkillIntentError, SkillSlotNotFound

class BaseSkill:
     name: str

     alex: AI
     intent: IntentResponse

     slots: dict[str, Slot] = {}

     def __init__(self):
          pass

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

     def responce(self, text):
          self.alex.set_context("last_renponce", text)
          self.alex.set_context("last_intent", self.intent)

          print(text)
