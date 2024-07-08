from random import choice
from core.ai.nexus import Nexus
from core.skills import BaseSkill
from core.api.client import ApiResponse
from core.intents.slots import SlotValue
from core.intents.responce import BoolResponce

class Get(BaseSkill):
     def __init__(self):
          self.register("dictionary@get")
          self.save_responce_for_context = False
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.require("word", SlotValue)
          self.meaning: ApiResponse = Nexus.request_ai("ALEX", "sendToApi", "dictionary/get/closest", self.slots["word"].value.lower())
          if self.meaning.response["name"] != None:
               if self.meaning.response["name"].lower() != self.slots["word"].value.lower():
                    self.question("not.equal", self.not_equal, {"word": self.meaning.response["name"]}, BoolResponce())
               else:
                   self.respond_meaning()
          else:
               self.responce_translated("not.found", {"word": self.slots["word"].value})

     def not_equal(self, responce: bool):
          if responce:
               self.respond_meaning()
          else:
               self.responce_translated("sorry.wrong.word")

     def respond_meaning(self):
          if self.is_list() and len(self.meaning.response['definition']) > 1:
               self.respond_multiple_meaning()
          else:
               self.respond_one_meaning()
     
     def is_list(self):
          return isinstance(self.meaning.response["definition"], list)
     
     def respond_one_meaning(self):
          definition = self.meaning.response["definition"] if not self.is_list() else self.meaning.response["definition"][0]
          self.responce(definition)
     
     def respond_multiple_meaning(self):
          self.question("multiple.meaning", self.multiple_meaning, {"number_of_meaning": len(self.meaning.response['definition'])}, BoolResponce())

     def multiple_meaning(self, responce: bool):
          types_os_joins = [", and we can say that it is, ", ", or, ", ", and it is, "]
          resp = ""
          if responce:
               i = 0
               for defs in self.meaning.response['definition']:
                    i += 1
                    if defs.endswith("."):
                         defs = defs[0:-1]
                    resp += defs + f"{choice(types_os_joins) if i < len(self.meaning.response['definition']) else ""}"
          else:
               resp = choice(self.meaning.response['definition'])
          self.responce(resp)
