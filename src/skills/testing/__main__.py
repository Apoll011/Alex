from core.system.intents import IntentResponse, Slot
from core.system.intents.slots import SlotValueNumber
from core.nexus.ai import AI

class SkillIntentError(Exception):
     def __init__(self, skill_name: str, name: str) -> None:
          super().__init__(f"This is the wrong skill({skill_name}) for this intent({name})")

class SkillSlotNotFound(Exception):
     def __init__(self, slot_name: str) -> None:
          super().__init__("The slot: " + slot_name + " was not found")

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
          print(self.intent)
          if slot_name in self.intent.slots.keys() and isinstance(self.intent.slots[slot_name].value, slot_type):
               self.slots[slot_name] = self.intent.slots[slot_name].value
          else:
               raise SkillSlotNotFound(slot_name)

class Skill(BaseSkill):
     def __init__(self):
          self.register("math@even_or_odd")
          super().__init__()

     def execute(self, alex: AI, intent: IntentResponse):
          super().execute(alex, intent)
          self.require("number", SlotValueNumber)

          if ((self.slots["number"].value % 2)==0):
               print(f"{self.slots["number"].value} is even")
          else:
               print(f"{self.slots["number"].value} is odd")
      