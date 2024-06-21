from core.system.intents.slots import SlotValueNumber, SlotValue
from core.system.skills import BaseSkill

class EvenOrOdd(BaseSkill):
     prime_search_limit = 5000

     def __init__(self):
          self.register("math@even.or.odd")
          super().__init__()

     def is_even(self):
          if self.slots["number"]:
               return ((self.slots["number"].value % 2)==0)

     def is_prime(self):
          if self.slots["number"].value > self.prime_search_limit:
               return self.responce_translated("search.limit")
          
          for i in range(2, int(self.slots["number"].value//2)):
               if self.slots["number"].value % i == 0:
                    return self.responce_translated(f"prime.no",self.slots["number"].value)
          
          return self.responce_translated(f"prime.yes",self.slots["number"].value)
               
     def execute(self, context, intent):
          super().execute(context, intent)
          self.require("number", SlotValueNumber)
          self.optional("type", SlotValue)

          if self.slots["type"] and self.slots["type"].value == "prime":
               r =  self.is_prime()
          elif self.slots["type"] and self.slots["type"].value == "even":
               r = self.make_responce("yes", "no")
          elif self.slots["type"] and self.slots["type"].value == "odd":
               r = self.make_responce("no", "yes")
          else:
               r = self.make_responce()
          return r
     def make_responce(self, first = "", second = ""):
          if self.slots["number"]:
               last = "odd"
               f = second
               if self.is_even():
                    last = "even"
                    f = first
               return self.responce_translated(f"responce.{f}.{last}", self.slots["number"].value)
              