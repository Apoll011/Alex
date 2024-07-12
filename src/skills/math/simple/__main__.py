from core.intents.slots import SlotValueNumber
from core.skills import BaseSkill

class Simple(BaseSkill):
     def init(self):
          self.register("math@simple")
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.require("mathoperation")
          self.optional("first_number", SlotValueNumber)
          self.optional("second_number", SlotValueNumber)
          self.optional("number", SlotValueNumber)
          
          self.mathOp = self.slots["mathoperation"]

          op = self.convert()

          r = None

          if self.slot_exists("number"):
               number: SlotValueNumber = self.slots["number"] # type: ignore
               last_result = self.alex_context.load("last_result")
               r = op(last_result, number.value)

          elif self.slot_exists("first_number", "second_number"):
               fNumber: SlotValueNumber = self.slots["first_number"] # type: ignore
               sNumber: SlotValueNumber = self.slots["second_number"] # type: ignore
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
          