from core.skills import BaseSkill

class HowAreU(BaseSkill):
     def init(self):
          self.register("saudation@how.are.u")
          self.can_go_again = False

     def execute(self, intent):
          super().execute(intent)

          self.say("fine")
          if self.alex().debug_mode:
              self.say("acknowledge")
