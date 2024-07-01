from core.system.intents.slots import SlotValueNumber, SlotValue
from core.system.skills import BaseSkill
from math import sin, cos, sqrt, cosh, sinh, tan, tanh

class Geometry(BaseSkill):
     def __init__(self):
          self.register("math@geometry")
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.require("func", SlotValue)
          self.require("number", SlotValueNumber)

          self.number: SlotValueNumber = self.slots["number"]

          r = None 

          if self.assert_equal("mathoperation", "sen"):
               r = sin(self.number.value)

          elif self.assert_equal("mathoperation", "cos"):
               r = cos(self.number.value)

          elif self.assert_equal("mathoperation", "sqrt"):
               r = sqrt(self.number.value)
          
          elif self.assert_equal("mathoperation", "tan"):
               r = tan(self.number.value)
          
          elif self.assert_equal("mathoperation", "tanh"):
               r = tanh(self.number.value)
          
          self.alex_context.save(r, "last_result")
          
          return self.responce_translated("result", {"result": r})

     