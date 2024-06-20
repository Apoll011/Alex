from core.system.skills.call import SkillCaller
from core.system.skills import BaseSkill

class Hi(BaseSkill):
     def __init__(self):
          self.register("saudation@hi")
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.responce(self.translate.get_translation("greet.hi", context.load("master")["name"]))
          
     def responce(self, text):
          self.speak(text)
