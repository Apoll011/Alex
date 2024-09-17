from math import cos, sin, sqrt, tan, tanh

from core.intents.slots import SlotValueNumber
from core.skills import BaseSkill

class Geometry(BaseSkill):
     def init(self):
          self.register("math@geometry")

     def execute(self, intent):
          super().execute(intent)
          self.require("func")
          self.optional("number", SlotValueNumber)

          if self.slot_exists("number"):
               self.number: SlotValueNumber = self.slots["number"] # type: ignore
          else:
               self.number: SlotValueNumber = self.alex_context.load("last_result") # type: ignore
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
          return SlotValueNumber("SlotValueNumber", float(r))
     