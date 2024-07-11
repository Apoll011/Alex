from core.intents.slots import SlotValueNumber
from core.skills import BaseSkill
from math import sin, cos, sqrt, cosh, sinh, tan, tanh

class Geometry(BaseSkill):
     def __init__(self):
          self.register("math@geometry")
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.require("func")
          self.require("number", SlotValueNumber)

          self.number: SlotValueNumber = self.slots["number"] # type: ignore

          r = None 

          if self.assert_equal("func", "sen"):
               r = sin(self.number.value)

          elif self.assert_equal("func", "cos"):
               r = cos(self.number.value)

          elif self.assert_equal("func", "sqrt"):
               r = sqrt(self.number.value)
          
          elif self.assert_equal("func", "tan"):
               r = tan(self.number.value)
          
          elif self.assert_equal("func", "tanh"):
               r = tanh(self.number.value)
          
          self.alex_context.save(r, "last_result")
          
          return self.responce_translated("result", {"result": r})

     