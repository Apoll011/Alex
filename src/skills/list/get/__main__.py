from core.skills import BaseSkill
from core.resources.data_files import List

class Get(BaseSkill):
     def init(self):
          self.register("list@get")
          self.can_go_again = False          

     def execute(self, context, intent):
          super().execute(context, intent)
          self.require("list")
          self.optional("entity")

          if List.exist(self.get("list")):
               if self.slot_exists("entity"):
                    self.check_element()
               else:
                    self.get_full_list()
          else:
               self.responce_translated("list.does.not.exist", {"list": self.get("list")})

     def check_element(self):
          if List.element_exists(self.get("list"), self.get("entity")):
               self.responce_translated("entity.exists", {"list": self.get("list"), "entity": self.get("entity")})
          else:
               self.responce_translated("entity.dont.exists", {"list": self.get("list"), "entity": self.get("entity")})
    
     def get_full_list(self):
          list_content = List.get(self.get("list"))
          ander = self.translate.get_translation("text.and")
          text = ", ".join(list_content[0:-1]) + f" {ander} " + list_content[-1]
          self.responce(text)
