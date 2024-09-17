import json
import os
import time
from pathlib import Path

from core.config import ATTENTION_WAIT_TIME, path as p
from core.context import ContextManager
from core.error import SkillIntentError, SkillSlotNotFound
from core.intents import *
from core.intents.responce import *
from core.interface.base import BaseInterface
from core.log import LOG
from core.translate import TranslationSystem

class BaseSkill:
     name: str

     alex_context: ContextManager
     intent: IntentResponse

     translate: TranslationSystem

     slots: dict[str, SlotValue] = {}

     can_go_again: bool

     can_repeat_responce = True

     skill_settings: dict

     language: str

     def __init__(self, language="en"):
          self.skill_dir = None
          self.language = language
          self.slots = {}
          self.name: str
          self.can_go_again = True
          self.skill_settings: dict = {}

          self.init()

     def init(self):
          ...

     def register(self, name):
          self.name = name
          path, skname = self.pretty_name(name)
          self.skill_dir = p + "/" + path
          self.get_local_settings()
          self.translate = TranslationSystem(self.language, "locale", path + "/assets/")

     def execute(self, intent: IntentResponse):
          context = self.alex().context
          if self.can_go_again:
               context.save(intent, "last_intent")
          if intent.intent.intent_name != self.name:
               raise SkillIntentError(self.name, intent.intent.intent_name)
          self.alex_context = context
          self.intent = intent

     def require(self, slot_name: str, slot_type=SlotValue):
          if slot_name in self.intent.slots.keys() and isinstance(
                  self.intent.slots[slot_name].value, slot_type
          ):
               self.slots[slot_name] = self.intent.slots[slot_name].value
          else:
               raise SkillSlotNotFound(slot_name)

     def optional(self, slot_name: str, slot_type=SlotValue):
          if slot_name in self.intent.slots.keys() and isinstance(
                  self.intent.slots[slot_name].value, slot_type
          ):
               self.slots[slot_name] = self.intent.slots[slot_name].value

     def question(
             self,
             key_to_question_to_ask,
             callback,
             question_replace=None,
             required_responce: Responce = AnyResponce(),
             *args,
     ):
          if question_replace is None:
               question_replace = {}
          required_responce.set_translation_system(self.alex().translationSystem)
          self.responce_translated(key_to_question_to_ask, question_replace)
          self.on_next_input(callback, required_responce, *args)

     def on_next_input(
             self, callback, required_responce: Responce = AnyResponce(), *args
     ):
          self.alex().setListenProcessor(callback, required_responce, *args)  # type: ignore

     def responce_translated(self, key: str, context=None):
          self.responce(self.translate.get_translation(key, context))

     def responce(self, text: str):
          text = text.strip()
          self.save_last_responce(text)
          self.speak(text)

     def speak(self, text):
          if not isinstance(text, dict):
               text = {"message": text}

          data = {"intent": self.intent.json, "voice": "Alex"} | text
          self.alex().speak(data)  # type: ignore

     def save_last_responce(self, text):
          if self.can_repeat_responce:
               self.alex_context.save(text, "last_responce")

     @staticmethod
     def pretty_name(name: str):
          s = name.split("@")
          skill_name = " ".join(s[1].split(".")).title().replace(" ", "")
          path = f"skills/{s[0]}/{s[1].replace('.', '_')}"
          return path, skill_name

     def get_raw_slot_value(self, slot_name: str):
          return self.intent.slots[slot_name].raw_value

     def get(self, slot_name: str):
          try:
               return self.slots[slot_name].value
          except KeyError:
               raise SkillSlotNotFound(slot_name)

     def slot_exists(self, *args: str):
          for a in args:
               if a not in self.slots.keys():
                    return False
          return True

     def assert_equal(self, slot_name: str, value: Any):
          if self.slots[slot_name].value == value:
               return True
          return False

     def assert_in(self, slot_name: str, obj_list: list):
          if self.slots[slot_name].value in obj_list:
               return True
          return False

     def assert_in_dict(self, slot_name: str, dictionary: dict):
          if self.slots[slot_name].value in dictionary.keys():
               return True
          return False

     def get_local_settings(self):
          """Build a dictionary using the JSON string stored in settings.json."""
          skill_settings = {}
          settings_path = Path(self.skill_dir).joinpath(".config")
          LOG.info(settings_path)
          if settings_path.exists():
               with open(str(settings_path)) as settings_file:
                    settings_file_content = settings_file.read()
               if settings_file_content:
                    try:
                         skill_settings = json.loads(settings_file_content)
                    except json.JSONDecodeError as error:
                         log_msg = f"Failed to load {self.name} settings from .config. LINE: {error.lineno}"
                         LOG.exception(log_msg)

          self.skill_settings = skill_settings

     def save_settings(self):
          """Save skill settings to file."""
          settings_path = Path(self.skill_dir).joinpath(".config")

          if not Path(settings_path).exists():
               settings_path.touch(mode=0o644)

          with open(str(settings_path), "w") as settings_file:
               try:
                    json.dump(self.skill_settings, settings_file)
               except Exception:
                    LOG.exception(
                         "error saving skill settings to " "{}".format(settings_path)
                    )
               else:
                    LOG.info(
                         "Skill settings successfully saved to " "{}".format(settings_path)
                    )

     @staticmethod
     def alex():
          return BaseInterface.get().alex

     def get_asset(self, name):
          path = f"{self.skill_dir}/assets/{name}"
          if os.path.isfile(path):
               return path
          else:
               raise FileNotFoundError(
                    f"The file {name} was not found in this skill assets pack."
               )

     def request_attention(self, require_confirmation=False):
          """
          Will call Master name and if the flag confirmation is set to True listen for a confirmation key word.
          """
          master_name: str = self.alex_context.load("master")["name"]  # type: ignore
          master_first_name = master_name.split()[0]
          self.responce(master_first_name)
          time.sleep(ATTENTION_WAIT_TIME)
          # TODO: Add require confirmation logic
