import importlib
from core.intents import IntentResponse
from core.context import ContextManager
from core.skills import BaseSkill

def prety_name(name: str):
    s = name.split("@")
    skillname = " ".join(s[1].split(".")).title().replace(" ", "")
    path = f"skills.{s[0]}.{s[1].replace(".", "_")}"
    return path, skillname


class SkillCaller:
    def __init__(self) -> None:
        pass

    def call(self, intent: IntentResponse):
        path, skillname = prety_name(intent.intent.intent_name)

        skill = importlib.import_module(path + ".__main__")

        instance: BaseSkill = getattr(skill, skillname)()

        return instance
