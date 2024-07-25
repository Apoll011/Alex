import os
from core.skills import BaseSkill
from core.resources.data_files import List
from core.intents.responce import BoolResponce

class Clear(BaseSkill):
     def init(self):
          self.register("list@clear")
          self.can_go_again = False          

     def execute(self, context, intent):
          super().execute(context, intent)
          self.optional("list")
          self.optional("entity")

          if not self.slot_exists("list"):
               self.question("get.list", self.get_list)
          else:
               self.list = self.get("list").lower()
               self.remove()

     def get_list(self, responce):
          self.list = responce.lower()
          self.remove()

     def remove(self):
          if self.slot_exists("entity"):
               self.entity = self.get("entity").lower()
               question = "entity"
               func = self.confirm_entity
          else:
               self.entity = ""
               question = "list"
               func = self.confirm_list
          
          if self.ensure_exists():
               self.question(f"confirm.{question}", func, {"entity": self.entity, "list": self.list}, BoolResponce())


     def ensure_exists(self) -> bool:
          if List.exist(self.list):
               if self.entity != "" and List.element_exists(self.list, self.entity):
                    return True
               elif self.entity == "":
                    return True
               else:
                    self.responce_translated("did.not.found.entity", {"list": self.list, "entity": self.entity})
          else:
               self.responce_translated("did.not.found.list", {"list": self.list})
          return False     

     def confirm_list(self, responce): 
          if responce:
               self.delete_list()
          else:
               self.responce_translated("dont.delete")

     def confirm_entity(self, responce):
          if responce:
               self.delete_entity()
          else:
               self.responce_translated("dont.delete")

     def delete_list(self):
          List.save(self.list, "", "w")
          self.responce_translated("delete.list", {"list": self.list})          

     def delete_entity(self):
          list_content = List.get(self.list)
          list_content.remove(self.entity)
          List.save(self.list, "\n".join(list_content), "w")
          self.responce_translated("delete.entity", {"list": self.list, "entity": self.entity})
