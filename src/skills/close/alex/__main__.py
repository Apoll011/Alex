from core.system.skills import BaseSkill
from core.system.ai.nexus import Nexus
from core.system.api.client import ApiClient
from core.system.intents.responce import BoolResponce

class Alex(BaseSkill):
     def __init__(self):
          self.register("close@alex")
          self.save_responce_for_context = False
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.question("close.server", self.after_responce, {}, BoolResponce())
     
     def after_responce(self, close_server):
          if close_server:
               pass 
          Nexus.call_ai("ALEX", "deactivate")
