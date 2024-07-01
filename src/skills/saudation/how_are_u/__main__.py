from core.system.skills import BaseSkill

class HowAreU(BaseSkill):
     def __init__(self):
          self.register("saudation@how.are.u")
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)

          self.responce_translated("under.contruction") 
