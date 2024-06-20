from core.system.intents.slots import SlotValueNumber, SlotValue
from core.system.skills import BaseSkill

class Simple(BaseSkill):
     def __init__(self):
          self.register("math@simple")
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.require("mathoperation", SlotValue)
          self.optional("first_number", SlotValueNumber)
          self.optional("second_number", SlotValueNumber)
          self.optional("number", SlotValueNumber)

          op = self.convert()

          r = None

          if self.slots["number"]:
               last_result = self.alex_context.load("last_result")
               r = op(last_result, self.slots["number"].value)

          elif self.slots["first_number"] and self.slots["second_number"]:
               r = op(self.slots["first_number"].value, self.slots["second_number"].value)
               self.alex_context.save(r, "last_result")
          
          self.responce(f"The result is {r}")

     def convert(self):
          if self.slots["mathoperation"].value == "plus":
               return lambda x, y: x + y 
          elif self.slots["mathoperation"].value == "times":
               return lambda x, y: x * y 
          elif self.slots["mathoperation"].value == "minus":
               return lambda x, y: x - y 
          elif self.slots["mathoperation"].value == "over":
               return lambda x, y: x / y 
          else:
               return lambda x, y: int(x) ^ int(y) 
          