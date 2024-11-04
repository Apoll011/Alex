from core.list import Item, Lists
from core.skills import BaseSkill

#TODO: Add quantity, maybe size, color, etc
class Add(BaseSkill):
    entity: str
    list: str
    list_obj: Lists
    def init(self):
        self.register("list@add")
        self.can_go_again = False
        self.list_obj = Lists.load()

    def execute(self, intent):
        super().execute(intent)
        self.optional("list")
        self.optional("entity")

        if not self.slot_exists("list") and not self.slot_exists("entity"):
            self.say("dont.have.data")
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
        self.list = self.get("list").strip().lstrip("a ")
        self.add_to_list()

    def add_to_list(self):
        list_name = self.list.lower()
        entity = self.entity.lower()
        self.list_obj.add_to_list(list_name, Item(entity))
        self.say("added.item", entity=entity.title(), list=list_name.title())
        self.list_obj.save()
