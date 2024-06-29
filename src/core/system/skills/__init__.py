from core.system.intents import *
from core.system.context import ContextManager
from .error import SkillIntentError, SkillSlotNotFound
from core.system.translate import TranslationSystem
from core.nexus.ai import Nexus
from typing import Any

class BaseSkill:
     name: str

     is_api: bool = False

     alex_context: ContextManager
     intent: IntentResponse

     translate: TranslationSystem

     slots: dict[str, Any] = {}

     def __init__(self):
          pass
     
     def set_as_api(self):
          self.is_api = True

     def execute(self, context: ContextManager, intent: IntentResponse):
          if intent.intent.intent_name != self.name:
               raise SkillIntentError(self.name, intent.intent.intent_name)
          self.alex_context = context
          self.intent = intent
               
     def register(self, name):
          self.name = name
          path, skname = self.prety_name(name)
          self.translate = TranslationSystem("en", "locale", path + "/assets/")
     
     def require(self, slot_name: str, slot_type):
          if slot_name in self.intent.slots.keys() and isinstance(self.intent.slots[slot_name].value, slot_type):
               self.slots[slot_name] = self.intent.slots[slot_name].value
          else:
               raise SkillSlotNotFound(slot_name)

     def optional(self, slot_name: str, slot_type):
          if slot_name in self.intent.slots.keys() and isinstance(self.intent.slots[slot_name].value, slot_type):
               self.slots[slot_name] = self.intent.slots[slot_name].value

     def responce(self, text: str):
          text = text.strip()
          if not self.is_api:
               self.set_as_last_intent(text)
               self.speak(text)
          return text
     
     def speak(self, text):
          Nexus.call_ai("ALEX", "speak", text)

     def responce_translated(self, key: str, *args):
          return self.responce(self.translate.get_translation(key, *args))

     def set_as_last_intent(self, text):
          self.alex_context.save(text, "last_responce")
          self.alex_context.save(self.intent, "last_intent")

     def prety_name(self, name: str):
          s = name.split("@")
          skillname = " ".join(s[1].split(".")).title().replace(" ", "")
          path = f"skills/{s[0]}/{s[1].replace(".", "_")}"
          return path, skillname

     def slot_exists(self, *args: str):
          for a in args:
               if a not in self.slots.keys():
                    return False
          return True
     
     def assert_equal(self, slot_name: str, value: Any):
          if self.slots[slot_name] == value:
               return True
          return False
