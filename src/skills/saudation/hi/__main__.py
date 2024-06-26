from core.system.skills import BaseSkill

class Hi(BaseSkill):
     def __init__(self):
          self.register("saudation@hi")
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.responce_translated("greet.hi", {"user": context.load("master")["name"]}) # type: ignore
          
     def responce(self, text):
          self.speak(text)
