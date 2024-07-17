import importlib
from core.log import LOG
from core.skills import BaseSkill
from core.intents import IntentResponse
from core.context import ContextManager

def prety_name(name: str):
    s = name.split("@")
    skillname = " ".join(s[1].split(".")).title().replace(" ", "")
    path = f"skills.{s[0]}.{s[1].replace(".", "_")}"
    return path, skillname


class SkillCaller:
    language: str

    def __init__(self, language = "en") -> None:
        self.language = language        

    def call(self, intent: IntentResponse):
        path, skillname = prety_name(intent.intent.intent_name)
        
        skill = importlib.import_module(path + ".__main__")
        instance: BaseSkill = getattr(skill, skillname)(self.language)
        
        return instance
