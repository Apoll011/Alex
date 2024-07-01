from core.system.skills import BaseSkill
from core.system.intents.slots import SlotValue

class Something(BaseSkill):
     def __init__(self):
          self.register("close@something")
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.require("entityName", SlotValue)
          
     def responce(self, text):
          self.speak(text)
