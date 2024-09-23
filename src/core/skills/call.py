import importlib

from core.error import MissingMainSkillClass
from core.intents import IntentResponse
from core.log import LOG
from core.skills import BaseSkill

class SkillCaller:
    language: str

    def __init__(self, language = "en") -> None:
        self.language = language        

    def call(self, intent: IntentResponse):
        LOG.info("Executing skill: " + intent.intent.intent_name)
        path, skill_name = self.get_skill_path_and_name(intent.intent.intent_name)
        
        try: 
            skill = importlib.import_module(path + ".__main__")
            instance: BaseSkill = getattr(skill, skill_name)(self.language)
        except AttributeError:
            raise MissingMainSkillClass(skill_name, intent.intent.intent_name)

        return instance

    @staticmethod
    def get_skill_path_and_name(name: str):
        s = name.split("@")
        skill_name = " ".join(s[1].split(".")).title().replace(" ", "")
        path = f"skills.{s[0]}.{s[1].replace('.', '_')}"
        return path, skill_name
