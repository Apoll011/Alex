from typing import Any
class Responce:

     rtype: Any
     replace = {

     }
     hard_search = False

     def is_accepted(self, text) -> bool:
          try:
               r = self.rtype(self.replace[self.parse(text)])
               if len(self.replace) > 0:
                    return True
               else:
                    return False
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
