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

          r = None 

          if self.slots['func'].value == "sen":
               r = sin(self.slots["number"].value)

          elif self.slots['func'].value == "cos":
               r = cos(self.slots["number"].value)

          elif self.slots['func'].value == "sqrt":
               r = sqrt(self.slots["number"].value)
          
          elif self.slots['func'].value == "tan":
               r = tan(self.slots["number"].value)
          
          elif self.slots['func'].value == "tanh":
               r = tanh(self.slots["number"].value)
          
          self.alex_context.save(r, "last_result")
          
          return self.responce_translated("result", r)

     