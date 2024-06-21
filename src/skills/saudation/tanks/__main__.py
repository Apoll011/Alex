from core.system.skills.call import SkillCaller
from core.system.skills import BaseSkill

class Tanks(BaseSkill):
     def __init__(self):
          self.register("saudation@tanks")
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.responce_translated("tank") # type: ignore
          
     def responce(self, text):
          self.speak(text)
