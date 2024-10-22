from core.skills import BaseSkill

class Tanks(BaseSkill):
     def init(self):
          self.register("saudation@tanks")
          self.can_go_again = False

     def execute(self, intent):
          super().execute(intent)
          self.say("thanks")
