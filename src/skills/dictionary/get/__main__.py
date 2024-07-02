from core.system.ai.nexus import Nexus
from core.system.skills import BaseSkill
from core.system.api.client import ApiResponse
from core.system.intents.slots import SlotValue

class Get(BaseSkill):
     def __init__(self):
          self.register("dictionary@get")
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.require("word", SlotValue)
          meaning: ApiResponse = Nexus.request_ai("ALEX", "sendToApi", "dictionary/get/closest", self.slots["word"].value)
          if meaning.response["name"] != None:
               definition = meaning.response["definition"]
               self.responce(definition)
          else:
               self.responce_translated("not.found", self.slots["word"].value)
