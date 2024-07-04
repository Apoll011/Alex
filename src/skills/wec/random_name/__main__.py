from core.system.skills import BaseSkill
from core.system.ai.nexus import Nexus
from core.system.intents.slots import SlotValue

class RandomName(BaseSkill):
     def __init__(self):
          self.register("wec@random.name")
          self.save_responce_for_context = False
          self.can_go_again = True
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.optional("gender")

          if self.slot_exists("gender"):
               name = Nexus.request_ai("WEC", "getName", self.slots["gender"].value)
          else:
               name = Nexus.request_ai("WEC", "getName", None)

          self.responce_translated("say.name", {"name": name})
