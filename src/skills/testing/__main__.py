from core.system.intents.slots import SlotValueNumber, SlotValue
from core.system.skills import BaseSkill

class EvenOrOdd(BaseSkill):
     prime_search_limit = 5000

     def __init__(self):
          self.register("math@even_or_odd")
          super().__init__()

     def is_even(self):
          if self.slots["number"]:
               return ((self.slots["number"].value % 2)==0)

     def is_prime(self):
          if self.slots["number"].value > self.prime_search_limit:
                    return self.responce("Sorry. This number is bigger than my upper search limit.")
          for i in range(2, self.slots["number"].value/2):
               if self.slots["number"].value % i == 0:
                    return self.responce(f"Yes {self.slots["number"].value} is prime")
               
     def execute(self, alex, intent):
          super().execute(alex, intent)
          self.require("number", SlotValueNumber)
          self.optional("type", SlotValue)

          if self.slots["type"] and self.slots["type"] == "prime":
               return self.is_prime()
          elif self.slots["type"] and self.slots["type"] == "even":
               self.make_responce("Yes", "No")
          elif self.slots["type"] and self.slots["type"] == "odd":
               self.make_responce("No", "Yes")
          else:
               self.make_responce()
     
     def make_responce(self, first = "", second = ""):
          if self.slots["number"]:
               if self.is_even():
                    return self.responce(f"{first} {self.slots["number"].value} is even")
               else:
                    return self.responce(f"{second} {self.slots["number"].value} is odd")
