from core.skills import BaseSkill

class Something(BaseSkill):
     def __init__(self):
          self.register("close@something")
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.require("entityName")
          
     def responce(self, text):
          self.speak(text)
