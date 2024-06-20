from core.system.intents.slots import SlotValueNumber
from core.system.skills import BaseSkill

class EvenOrOdd(BaseSkill):
     def __init__(self):
          self.register("math@even_or_odd")
          super().__init__()

     def execute(self, alex, intent):
          super().execute(alex, intent)
          self.require("number", SlotValueNumber)

          if ((self.slots["number"].value % 2)==0):
               self.responce(f"{self.slots["number"].value} is even")
          else:
               self.responce(f"{self.slots["number"].value} is odd")
