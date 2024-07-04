import json
from typing import Any
from pathlib import Path
from core.system.log import LOG
from core.system.intents import *
from core.system.ai.nexus import Nexus
from core.system.intents.responce import *
from core.system.context import ContextManager
from core.system.config import path as p
from .error import SkillIntentError, SkillSlotNotFound
from core.system.translate import TranslationSystem

class BaseSkill:
     name: str

     is_api: bool = False

     alex_context: ContextManager
     intent: IntentResponse

     translate: TranslationSystem

     slots: dict[str, Any] = {}

     save_responce_for_context = True

     can_go_again = False

     skill_settings: dict 

     def __init__(self):
          self.slots = {}
          self.name: str
          self.is_api: bool = False
          self.save_responce_for_context = True
          self.can_go_again = False
          self.skill_settings: dict = {}
     
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
          self.skill_dir = p + "/" + path
          self.get_local_settings()
          self.translate = TranslationSystem("en", "locale", path + "/assets/")
     
     def require(self, slot_name: str, slot_type):
          if slot_name in self.intent.slots.keys() and isinstance(self.intent.slots[slot_name].value, slot_type):
               self.slots[slot_name] = self.intent.slots[slot_name].value
          else:
               raise SkillSlotNotFound(slot_name)

     def optional(self, slot_name: str, slot_type = SlotValue):
          if slot_name in self.intent.slots.keys() and isinstance(self.intent.slots[slot_name].value, slot_type):
               self.slots[slot_name] = self.intent.slots[slot_name].value

     def responce(self, text: str):
          text = text.strip()
          if not self.is_api:
               if self.save_responce_for_context:
                    self.set_as_last_intent(text)
               if self.can_go_again:
                    self.set_as_last_intent_repeater(text)
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

     def set_as_last_intent_repeater(self, text):
          self.alex_context.save(text, "last_responce_repeater")
          self.alex_context.save(self.intent, "last_intent_repeater")

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

     def question(self, key_to_question_to_ask, callback, question_replacers = {}, required_responce:Responce = AnyResponce(), *args):
          self.responce_translated(key_to_question_to_ask, question_replacers)
          Nexus.call_ai("ALEX", "setListenProcessor", callback, required_responce, *args)
     
     def get_local_settings(self):
          """Build a dictionary using the JSON string stored in settings.json."""
          skill_settings = {}
          settings_path = Path(self.skill_dir).joinpath('settings.json')
          LOG.info(settings_path)
          if settings_path.exists():
               with open(str(settings_path)) as settings_file:
                    settings_file_content = settings_file.read()
               if settings_file_content:
                    try:
                         skill_settings = json.loads(settings_file_content)
                    # TODO change to check for JSONDecodeError in 19.08
                    except Exception:
                         log_msg = 'Failed to load {} settings from settings.json'
                         LOG.exception(log_msg.format(self.name))

          self.skill_settings = skill_settings


     def save_settings(self):
          """Save skill settings to file."""
          settings_path = Path(self.skill_dir).joinpath('settings.json')

          if not Path(settings_path).exists():
               settings_path.touch(mode=0o644)

          with open(str(settings_path), 'w') as settings_file:
               try:
                    json.dump(self.skill_settings, settings_file)
               except Exception:
                    LOG.exception('error saving skill settings to '
                                   '{}'.format(settings_path))
               else:
                    LOG.info('Skill settings successfully saved to '
                              '{}' .format(settings_path))
