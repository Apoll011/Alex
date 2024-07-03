from typing import Any
from core.system.intents.responce import *
from core.system.intents import *
from core.system.context import ContextManager
from .error import SkillIntentError, SkillSlotNotFound
from core.system.translate import TranslationSystem
from core.system.ai.nexus import Nexus

class BaseSkill:
     name: str

     is_api: bool = False

     alex_context: ContextManager
     intent: IntentResponse

     translate: TranslationSystem

     slots: dict[str, Any] = {}

     save_responce_for_context = True

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
               if self.save_responce_for_context:
                    self.set_as_last_intent(text)
               self.speak(text)
          return text
     
     def speak(self, text):
          if not isinstance(text, dict):
               text = {
                    "message": text
               }
          
          data = {
               "intent": self.intent.json,
               "voice": "Alex"
          } | text
          Nexus.call_ai("ALEX", "speak", data)

     def responce_translated(self, key: str, context = None):
          return self.responce(self.translate.get_translation(key, context))

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
          if self.slots[slot_name].value == value:
               return True
          return False

     def assert_in(self, slot_name: str, list: list):
          if self.slots[slot_name].value in list:
               return True
          return False

     def assert_in_dict(self, slot_name: str, dictionary: dict):
          if self.slots[slot_name].value in dictionary.keys():
               return True
          return False

     def question(self, key_to_question_to_ask, callback, question_replacers = {}, required_responce:Responce = AnyReponce(), *args):
          self.responce_translated(key_to_question_to_ask, question_replacers)
          Nexus.call_ai("ALEX", "setListenProcessor", callback, required_responce, *args)
