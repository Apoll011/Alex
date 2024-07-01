from core.system.skills import BaseSkill
from core.system.ai.nexus import Nexus
from core.system.api.client import ApiClient
from core.system.intents.responce import BoolReponce

class Alex(BaseSkill):
     def __init__(self):
          self.register("close@alex")
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.question("close.server", self.after_responce, {}, BoolReponce())
     
     def after_responce(self, close_server):
          if close_server:
               pass
          else:
               Nexus.call_ai("ALEX", "deactivate")

     def responce(self, text):
          self.speak(text)
