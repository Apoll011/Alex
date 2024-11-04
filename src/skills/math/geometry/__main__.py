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
              self.number: SlotValueNumber = self.get_obj("number")
          else:
              self.number: SlotValueNumber = self.context_load("last_result")
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

          self.context_save("last_result", r)

          return self.say("result", result=r)

     @staticmethod
     def round(result):
          r = "{:.4f}".format(result)
          return SlotValueNumber("SlotValueNumber", float(r))
     