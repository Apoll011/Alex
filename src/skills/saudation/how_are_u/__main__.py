from core.skills import BaseSkill

class HowAreU(BaseSkill):
     def init(self):
          self.register("saudation@how.are.u")
          self.can_go_again = False

     def execute(self, intent):
          super().execute(intent)

          self.responce_translated("fine")
          self.responce_translated("acknowledge")
