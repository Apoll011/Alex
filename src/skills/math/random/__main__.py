from random import randint, random
from core.skills import BaseSkill
from core.intents.slots import SlotValueNumber

class Random(BaseSkill):
     def init(self):
          
          self.register("math@random")
          
     def execute(self, context, intent):
          super().execute(context, intent)
          self.optional("smaller_number", SlotValueNumber)
          self.optional("bigger_number", SlotValueNumber)
          self.optional("type")
          self.optional("sign")

          result = 0

          required_signal = self.convert_signal()
          required_type = self.convert_type()
          smaller_number, bigger_number = self.getnumber_range()

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
          
          result = self.int_or_float(result)

          self.alex_context.save(result, "last_result")
          self.responce_translated("tell.result", {"result": str(result) + ("i" if required_type == "imaginary" else "")})
     
     def convert_signal(self):
          if self.slot_exists("sign"):
               if self.assert_equal("sign", "positive"):
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
               return (int(self.slots["smaller_number"].get_value()), int(self.slots["bigger_number"].get_value())) # type: ignore
          return self.skill_settings['min'], self.skill_settings["max"]
     
     def round(self, result):
          r = "{:.4f}".format(result)
          return float(r)

     def int_or_float(self, value):
        return int(value) if (value % 1) == 0 else self.round(value)
