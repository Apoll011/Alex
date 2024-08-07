from core.skills import BaseSkill
from core.resources.data_files import List

#TODO: Add quantity, maybe size, color, etc
class Add(BaseSkill):
     def init(self):
          self.register("list@add")
          self.can_go_again = False          

     def execute(self, context, intent):
          super().execute(context, intent)
          self.optional("list")
          self.optional("entity")

          if not self.slot_exists("list") and not self.slot_exists("entity"):
               self.responce_translated("dont.have.data")
          elif not self.slot_exists("list"):
               self.question("get.list", self.get_list, {"entity": self.get("entity")})
          elif not self.slot_exists("entity"):
               self.question("get.entity", self.get_entity, {"list": self.get("list")})
          else:
               self.entity = self.get("entity")
               self.list = self.get("list")
               self.add_to_list()

     def get_list(self, responce):
          self.list = responce.replace("list", "").strip()
          self.entity = self.get("entity")
          self.add_to_list()

     def get_entity(self, responce):
          self.entity = responce
          self.list = self.get("list")
          self.add_to_list()

     def add_to_list(self):
          list = self.list.lower()
          entity = self.entity.lower()
          List.append(list, entity)
          self.responce_translated("added.item", {"entity": entity.title(), "list": list.title()})
