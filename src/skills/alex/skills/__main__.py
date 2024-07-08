import os
from core.config import path
from core.skills import BaseSkill
from core.intents import SlotValue

class Skills(BaseSkill):
     def __init__(self):
          self.register("alex@skills")
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.require("major_skill", SlotValue)
          self.optional("minor_skill", SlotValue)
          
          if not self.slot_exists("minor_skill"):
               self.look_for_major(self.respond_based_on_minors)
          else:
               self.look_for_major(self.respond_based_on_minor)
               
     def look_for_major(self, func):
          major_list = os.listdir(path+"/skills/")
          if self.assert_in("major_skill", major_list):
               func()
          else:
               self.responce_translated("not.found")

     def respond_based_on_minors(self):
          minors = self.get_minor(self.slots["major_skill"].value)
          if len(minors) == 0:
               self.responce_translated("yes.avaliable", {"major": self.slots["major_skill"], "minor": minors[0]})
          else:
               self.responce_translated("yes.avaliables", {"major": self.slots["major_skill"], "minors": self.format(minors)})
     
     def respond_based_on_minor(self):
          minors = self.get_minor(self.slots["major_skill"].value)
          if self.assert_in("minor_skill", minors):
               self.responce_translated("yes.avaliable.one", {"major": self.slots["major_skill"], "minor": self.slots["minor_skill"]})
          else:
               self.responce_translated("not.found")

     def responce(self, text):
          self.speak(text)
     
     def get_minor(self, major):
          l =  map(
               lambda x: " ".join(x.split("_")), 
               list(
                    filter(
                         lambda obj: os.path.isdir(path+"/skills/"+major+"/"+obj), 
                         os.listdir(path+"/skills/"+major+"/")
                         )
                    )
               )
          l = list(l)
          try:
               l.remove("  pycache  ")
          except:
               pass
          return l

     def format(self, list: list):
          return ", ".join(list)
