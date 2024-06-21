from core.system.skills.call import SkillCaller
from core.system.skills import BaseSkill

class HowAreU(BaseSkill):
     def __init__(self):
          self.register("saudation@how.are.you")
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)

          self.responce("The AI HIANE is not set yet. We from Nexus apreciate your pacience while your creator is working on it.")   
