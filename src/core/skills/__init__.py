import json
import os
import time
from pathlib import Path
from threading import Thread

from core.client import ApiMethod
from core.config import ATTENTION_WAIT_TIME
from core.error import SkillIntentError, SkillNotRegistered, SkillSlotNotFound
from core.intents import *
from core.intents.responce import *
from core.interface.base import BaseInterface
from core.log import LOG
from core.notifier import AlexEvent
from core.translate import TranslationSystem
from core.utils import resource_path

class BaseSkill:
    # Private Variables
    name: str

    intent: IntentResponse

    translate: TranslationSystem

    slots: dict[str, SlotValue] = {}

    skill_dir: str | None = None

    skill_settings: dict = {}

    language: str

    is_registered = False

    # Public for editing variables
    can_repeat_responce = True
    can_go_again: bool = True
    voice = "Alex"

    # Private:
    def __init__(self, language="en"):
        self.language = language

        self.init()

    def init(self):
        ...

    def register(self, name):
        self.name = name
        path, skname = self.pretty_name(name)
        self.skill_dir = resource_path(f"skills/{path}")
        self.get_local_settings()
        self.translate = TranslationSystem(self.language, "locale", f"{self.skill_dir}/assets/")
        self.is_registered = True

    def execute(self, intent: IntentResponse):
        if not self.is_registered:
            raise SkillNotRegistered(intent.intent.intent_name)
        if self.can_go_again:
            self.context_save("last_intent", intent)
        if intent.intent.intent_name != self.name:
            raise SkillIntentError(self.name, intent.intent.intent_name)
        self.intent = intent

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

    def responce_translated(self, key: str, context=None):
        self.responce(self.translate.get_translation(key, context))

    def responce(self, text: str):
        text = self.process_text(text)
        self.save_last_responce(text)
        self.speak(text)

    @staticmethod
    def process_text(text: str) -> str:
        # Change "'" to something else
        text = text.replace("'", "").strip()
        # Fix spacing
        return text

    def speak(self, text):
        if not isinstance(text, dict):
            text = {"message": text}

        data = {"intent": self.intent.json, "voice": self.voice} | text
        self.alex().speak(data)  # type: ignore

    def save_last_responce(self, text):
        if self.can_repeat_responce:
            self.context_save("last_responce", text)

    @staticmethod
    def pretty_name(name: str):
        s = name.split("@")
        skill_name = " ".join(s[1].split(".")).title().replace(" ", "")
        path = f"{s[0]}/{s[1].replace('.', '_')}"
        return path, skill_name

    # Public
    def require(self, slot_name: str, slot_type=SlotValue):
        if slot_name in self.intent.slots.keys() and isinstance(
                self.intent.slots[slot_name].value, slot_type
        ):
            self.slots[slot_name] = self.intent.slots[slot_name].value
        else:
            slot_language_name = self.translate.get_translation(slot_name, return_none=True) or slot_name
            raise SkillSlotNotFound(slot_language_name)

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
        self.alex().text_processor.setListenProcessor(callback, required_responce, *args)  # type: ignore

    def say(self, key, **kwargs):
        self.responce_translated(key, kwargs)

    def get(self, slot_name: str, raw=False):
        try:
            if raw:
                return self.intent.slots[slot_name].raw_value
            return self.slots[slot_name].value
        except KeyError:
            raise SkillSlotNotFound(slot_name)

    def get_obj(self, slot_name):
        try:
            return self.slots[slot_name]
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

    def get_asset(self, name):
        path = f"{self.skill_dir}/assets/{name}"
        if os.path.isfile(path):
            return path
        else:
            raise FileNotFoundError(
                f"The file {name} was not found in this skill assets pack."
            )

    def request_attention(self):
        """
        Will call Master name and if the flag confirmation is set to True listen for a confirmation key word.
        """
        master_name: str = self.context_load("master").name
        master_first_name = master_name.split()[0]
        self.responce(master_first_name)
        time.sleep(ATTENTION_WAIT_TIME)

    def register_event(self, event: AlexEvent):
        Thread(target=self.alex().notifier.event, args=[event]).start()

    def api(self, route, method=ApiMethod.GET, **kwargs):
        return self.alex().api.call_route(route, kwargs, method)

    def config(self, config_name):
        try:
            config = self.skill_settings["config"][config_name]

            match config["type"]:
                case "number":
                    if (
                            ("min" in config.keys() and config["min"] <= config["value"])
                            or ("min" not in config.keys())
                    ) and (
                            ("max" in config.keys() and config["max"] >= config["value"])
                            or ("max" not in config.keys())
                    ):
                        return config["value"]
                    else:
                        return config["default"]
                case "text":
                    return config["value"] if config["value"] and config["value"].strip() != "" else config["default"]
                case "bool":
                    if not (config["value"] == 1 or config["value"] == 0):
                        return bool(config["default"])
                    else:
                        return config["value"]
                case _:
                    raise ValueError("Unknown type for configuration:", config["type"])
        except (KeyError, ValueError):
            return None

    def context_save(self, name: str, obj):
        self.alex().context.save(obj, name)

    def context_load(self, name: str):
        return self.alex().context.load(name)

    def setting(self, name):
        return self.skill_settings[name]

    def save_setting(self, name, value):
        self.skill_settings[name] = value
        self.save_settings()

    def save_config(self, name, value):
        config = self.skill_settings["config"][name]

        match config["type"]:
            case "number":
                if (
                        ("min" in config.keys() and config["min"] <= value)
                        or ("min" not in config.keys())
                ) and (
                        ("max" in config.keys() and config["max"] >= value)
                        or ("max" not in config.keys())
                ):
                    self.skill_settings["config"][name]["value"] = value
                else:
                    raise ValueError("The value provided does not match the requested by the config parameters")
            case "text":
                self.skill_settings["config"][name]["value"] = value

            case "bool":
                if type(value) == bool:
                    self.skill_settings["config"][name]["value"] = value
                else:
                    raise ValueError("The value provided does not match the requested by the config parameters")
            case _:
                raise ValueError("Unknown type for configuration:", config["type"])

        self.save_settings()

    def get_language(self):
        return self.language

    def dir(self):
        return self.skill_dir

    def get_translation(self, key: str, context=None, return_none=False, fallback=None) -> str:
        """
        Retrieves a translation for a given key.

        :param key: The translation key
        :param context: Optional arguments to format the translation string
        :param return_none: If key is not found return None
        :param fallback: The translation utilized in case the requested was not found,

        :return: The translated string

        :raises KeyError: If the key is not found on the dictionary and raise_error is set to True.
        """
        return self.translate.get_translation(key, context, return_none, fallback)

    @staticmethod
    def play_audio(path):
        BaseInterface.get().process(
            {
                "type": "play_audio",
                "path": path,
            }
        )
