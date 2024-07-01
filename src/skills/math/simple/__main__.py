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
          
          self.mathOp: SlotValue = self.slots["mathoperation"]

          op = self.convert()

          r = None

          if self.slot_exists("number"):
               number: SlotValueNumber = self.slots["number"]
               last_result = self.alex_context.load("last_result")
               r = op(last_result, number.value)

          elif self.slot_exists("first_number", "second_number"):
               fNumber: SlotValueNumber = self.slots["first_number"]
               sNumber: SlotValueNumber = self.slots["second_number"]
               r = op(fNumber.value, sNumber.value)
               self.alex_context.save(r, "last_result")
          return self.responce_translated("result", {"result": r})

     def convert(self):
          if self.assert_equal("mathoperation", "plus"):
               return lambda x, y: x + y 
          elif self.assert_equal("mathoperation", "times"):
               return lambda x, y: x * y 
          elif self.assert_equal("mathoperation", "minus"):
               return lambda x, y: x - y 
          elif self.assert_equal("mathoperation", "over"):
               return lambda x, y: x / y 
          else:
               return lambda x, y: int(x) ^ int(y) 
          