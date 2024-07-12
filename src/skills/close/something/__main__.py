from core.skills import BaseSkill

class Something(BaseSkill):
     def init(self):
          self.register("close@something")
          

     def execute(self, context, intent):
          super().execute(context, intent)
          self.require("entityName")
          
     def responce(self, text):
          self.speak(text)
