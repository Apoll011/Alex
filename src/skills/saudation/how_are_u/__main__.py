from core.skills import BaseSkill

class HowAreU(BaseSkill):
     def init(self):
          self.register("saudation@how.are.u")
          

     def execute(self, context, intent):
          super().execute(context, intent)

          self.responce_translated("under.contruction") 
