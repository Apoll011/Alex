from random import randint, random
from core.system.skills import BaseSkill
from core.system.intents.slots import SlotValueNumber

class Random(BaseSkill):
     def __init__(self):
          self.register("math@random")
          self.can_go_again = True
          self.save_responce_for_context = False
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.optional("smaller_number", SlotValueNumber)
          self.optional("bigger_number", SlotValueNumber)
          self.optional("type")
          self.optional("signal")

          result = 0

          required_signal = self.convert_signal()
          required_type = self.convert_type()
          number_range = self.getnumber_range()

          if number_range:
               smaller_number, bigger_number = number_range
          else:
               smaller_number, bigger_number = self.skill_settings['min'], self.skill_settings["max"]

          if required_type == "even":
               result = randint(smaller_number // 2 * 2, bigger_number // 2 * 2)
          elif required_type == "odd":
               result = randint(smaller_number // 2 * 2 + 1, bigger_number // 2 * 2 + 1)
          elif required_type == "prime":
               pass
          elif required_type == "real":
               result = randint(smaller_number, bigger_number)  * random()     
          else:
               result = randint(smaller_number, bigger_number)

          if required_signal == "+":
               result = abs(result)
          elif required_signal == "-":
               result = -abs(result)

          self.alex_context.save(result, "last_result")
          self.responce_translated("tell.result", {"result": str(result) + ("i" if required_type == "imaginary" else "")})

     def convert_signal(self):
          if self.slot_exists("signal"):
               if self.assert_equal("signal", "positive"):
                    return "+"
               else:
                    return "-"
          return None

     def convert_type(self):
          if self.slot_exists("type"):
               return self.slots["type"].value
          return None

     def getnumber_range(self):
          if self.slot_exists("smaller_number") and self.slot_exists("bigger_number"):
               return (int(self.slots["smaller_number"].value), int(self.slots["bigger_number"].value))
          return None