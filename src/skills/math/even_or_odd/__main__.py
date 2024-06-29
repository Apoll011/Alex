from core.system.intents.slots import SlotValueNumber, SlotValue
from core.system.skills import BaseSkill

class EvenOrOdd(BaseSkill):
     prime_search_limit = 5000

     def __init__(self):
          self.register("math@even.or.odd")
          super().__init__()

     def is_prime(self):
          if self.number.value > self.prime_search_limit:
               return self.responce_translated("search.limit")
          
          for i in range(2, int(self.number.value//2)):
               if self.number.value % i == 0:
                    return self.responce_translated(f"prime.no", self.number.value)
          
          return self.responce_translated(f"prime.yes", self.number.value)
               
     def execute(self, context, intent):
          super().execute(context, intent)
          self.require("number", SlotValueNumber)
          self.optional("type", SlotValue)

          self.number: SlotValueNumber = self.slots["number"] # type: ignore

          if self.slot_exists("type") and self.assert_equal("type", "prime"):
               r =  self.is_prime()
          elif self.slot_exists("type") and self.assert_equal("type", "even"):
               r = self.make_responce("yes", "no")
          elif self.slot_exists("type") and self.assert_equal("type", "odd"):
               r = self.make_responce("no", "yes")
          else:
               r = self.make_responce()
          return r
     
     def make_responce(self, first = "", second = ""):
          last = "odd"
          f = second
          if self.number.is_even():
               last = "even"
               f = first
          return self.responce_translated(f"responce.{f}.{last}", self.number.value)
              