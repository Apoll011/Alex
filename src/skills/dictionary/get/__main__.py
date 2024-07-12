from random import choice
from core.skills import BaseSkill
from core.api.client import ApiResponse
from core.interface.base import BaseInterface
from core.intents.responce import BoolResponce, SomethingFromListOrNoneResponce

class Get(BaseSkill):
     def init(self):
          self.register("dictionary@get")
          self.save_responce_for_context = False
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.require("word")
          self.get_meaning(self.slots["word"].value)

     def get_meaning(self, word):
          self.meaning: ApiResponse = BaseInterface.get().alex.handle_request("sendToApi", "dictionary/get/closest", word.lower())
          self.requested = word
          if self.meaning.response["name"] != None:
               if self.meaning.response["name"].lower() != self.requested.lower():
                    self.question("not.equal", self.not_equal, {"word": self.meaning.response["name"]}, BoolResponce())
               else:
                   self.respond_meaning()
          else:
               self.responce_translated("not.found", {"word": self.requested})

     def not_equal(self, responce: bool):
          if responce:
               self.respond_meaning()
          else:
               others = self.meaning.response["others"]
               if len(others) == 0:
                    self.responce_translated("not.found", {"word": self.requested})
               elif len(others) == 1:
                    self.question("other.match", self.get_meaning_from_question, {"word": others[0]}, BoolResponce(), others[0])
               else:
                    self.question("other.matchs", self.get_meanig_of_one_word, {"words": ", ".join(others)}, SomethingFromListOrNoneResponce(others))
     
     def get_meaning_from_question(self, responce: bool, word):
          if responce:
               self.get_meaning(word)
          else:
               self.responce_translated("sorry.not.have.word")
     
     def get_meanig_of_one_word(self, responce: str | None):
          if responce == None:
               self.responce_translated("sorry.not.have.word")
          else:
               print(responce)
               self.get_meaning(responce)
     
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
