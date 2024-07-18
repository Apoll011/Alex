from core.skills import BaseSkill
from core.intents.slots import SlotValueNumber
from math import sin, cos, sqrt, cosh, sinh, tan, tanh

class Geometry(BaseSkill):
     def init(self):
          self.register("math@geometry")
          

     def execute(self, context, intent):
          super().execute(context, intent)
          self.require("func")
          self.require("number", SlotValueNumber)

          self.number: SlotValueNumber = self.slots["number"] # type: ignore

          r = None 

          if self.assert_equal("func", "sen"):
               r = sin(self.number.get_value())

          elif self.assert_equal("func", "cos"):
               r = cos(self.number.get_value())

          elif self.assert_equal("func", "sqrt"):
               r = sqrt(self.number.get_value())
          
          elif self.assert_equal("func", "tan"):
               r = tan(self.number.get_value())
          
          elif self.assert_equal("func", "tanh"):
               r = tanh(self.number.get_value())
          
          r = self.round(r)
          
          self.alex_context.save(r, "last_result")
          
          return self.responce_translated("result", {"result": r})

     def round(self, result):
          r = "{:.4f}".format(result)
          return float(r)
     