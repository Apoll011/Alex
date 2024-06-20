from skills.testing.__main__ import EvenOrOdd
from core.system.skills import BaseSkill

class Skill(BaseSkill):
     def __init__(self):
          self.register("math@even_or_odd")
          super().__init__()

     def execute(self, alex, intent):
          super().execute(alex, intent)

          last_responce = self.alex.get_context("last_responce")
          last_intent = self.alex.get_context("last_intent")

          skill = EvenOrOdd()
          skill.set_as_api()
          new_value = skill.execute(alex, last_intent) # type: ignore

          if new_value  == last_responce: 
               self.responce("Yes")
          
          else:
               self.responce(f"Sorry. The correct anwser is: {new_value}")

     def responce(self, text):
          self.speak(text)
