from core.system.skills import BaseSkill
from core.system.intents.responce import BoolReponce

class Alex(BaseSkill):
     def __init__(self):
          self.register("close@alex")
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.question("close.server", self.after_responce, {}, BoolReponce())
     
     def after_responce(self, responce):
          self.responce(responce)

     def responce(self, text):
          self.speak(text)
