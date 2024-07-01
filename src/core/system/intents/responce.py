from typing import Any
class Responce:

     rtype: Any
     rvalue = []
     replace = {

     }

     def is_accepted(self, text) -> bool:
          try:
               r = self.rtype(self.parse(text))
               if len(self.rvalue) > 0 and text.lower() in self.rvalue:
                    return True
               else:
                    return False
          except:
               return False
     
     def parse(self, text):
          return self.replace[text.lower()]

class AnyReponce(Responce):
     rtype = lambda x: x

class BoolReponce(Responce):
     replace = {
          "yes": True,
          "no": False
     }
     rtype = bool
     rvalue = ["yes", "no"]
