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

class AnyResponce(Responce):
     def is_accepted(self, text) -> bool:
          self.result = text
          return True

class SomethingFromListOrNoneResponce(Responce):
     replace = {
          "none": None,
     }

     def __init__(self, list_word) -> None:
          for e in list_word:
               self.replace.update({e: 1})
          self.list = list_word

     def is_accepted(self, text) -> bool:
          if "none" in text.lower():
               self.result = None
               return True
          
          for elem in self.list:
               if text.lower() in elem.lower():
                    self.result = text
                    return True
          
          return False

class SomethingOrNoneResponce(Responce):
     def is_accepted(self, text) -> bool:
          self.result = text
          if "none" in text:
               self.result = None
          return True

class BoolResponce(Responce):
     replace = {
          "yes": True,
          "no": False
     }
     rtype = bool
