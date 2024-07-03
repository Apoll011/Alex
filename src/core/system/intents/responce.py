from typing import Any
class Responce:

     rtype: Any
     replace = {

     }
     hard_search = False

     result: Any

     def is_accepted(self, text) -> bool:
          try:
               if len(self.replace) > 0: 
                    self.result = self.rtype(self.replace[self.parse(text)])
               else:
                    self.result = self.rtype(self.parse(text))
               return True
          except:
               return False
     
     def parse(self, text):
          if len(self.replace) > 0:
               if self.hard_search:
                    return text.lower()
               else:
                    for e in self.replace.keys():
                         if e in text.lower():
                              return e
          else: 
               return text

class AnyReponce(Responce):
     rtype = lambda x: x

class BoolReponce(Responce):
     replace = {
          "yes": True,
          "no": False
     }
     rtype = bool
