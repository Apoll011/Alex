from core.skills import BaseSkill
from plugins.list import Lists, NoElements

class Get(BaseSkill):
     def init(self):
          self.register("list@get")
          self.can_go_again = False
          self.list_obj = Lists.load()          

     def execute(self, context, intent):
          super().execute(context, intent)
          self.require("list")
          self.optional("entity")

          if self.list_obj.get(self.get("list")):
               if self.slot_exists("entity"):
                    self.check_element()
               else:
                    self.get_full_list()
          else:
               self.responce_translated("list.does.not.exist", {"list": self.get("list")})

     def check_element(self):
          if self.list_obj.get(self.get("list"), self.get("entity")):
               self.responce_translated("entity.exists", {"list": self.get("list"), "entity": self.get("entity")})
          else:
               self.responce_translated("entity.dont.exists", {"list": self.get("list"), "entity": self.get("entity")})
    
     def get_full_list(self):
          try:
               text:str = self.list_obj.get(self.get("list")) # type: ignore
               self.responce(text)
          except NoElements:
               self.responce(self.translate("no.elements", {"list": self.get("list")}))
