from core.intents.responce import BoolResponce
from core.resources.data_files import List
from core.skills import BaseSkill

class Update(BaseSkill):
    def init(self):
        self.register("list@update")
        self.can_go_again = False

    def execute(self, intent):
        super().execute(intent)
        self.optional("list")
        self.optional("entity")
        self.optional("new_entity")

        if not self.slot_exists("list") and not self.slot_exists("entity") and not self.slot_exists(
                "new_entity"
        ):
            self.say("dont.have.data")
        elif not self.slot_exists("list"):
            self.question("get.list", self.get_list)
        elif not self.slot_exists("entity"):
            self.question(
                "get.entity", self.get_entity, {
                    "list": self.get("list"),
                    "new": self.get("new_entity")
                }
            )
        elif not self.slot_exists("new_entity"):
            self.question(
                "get.new.entity", self.get_new_entity, {
                    "list": self.get("list"),
                    "entity": self.get("entity")
                }
            )
        else:
            self.entity = self.get("entity")
            self.list = self.get("list")
            self.new = self.get("new_entity")
            self.update_element()

    def get_list(self, responce):
        self.list = responce.replace("list", "").strip()
        self.entity = self.get("entity")
        self.new = self.get("new_entity")
        self.update_element()

    def get_entity(self, responce):
        self.entity = responce
        self.list = self.get("list")
        self.new = self.get("new_entity")
        self.update_element()

    def get_new_entity(self, responce):
        self.new = responce
        self.list = self.get("list")
        self.entity = self.get("entity")
        self.update_element()

    def update_element(self):
        list_element = self.list.lower()
        entity = self.entity.lower()
        new = self.new.lower()
        if List.exist(list_element):
            try:
                self.try_to_update(list_element, entity, new)

            except ValueError:
                self.question(
                    "did.not.found.entity", self.add_new, {
                        "list": list_element,
                        "entity": entity,
                        "new": new,
                    }, BoolResponce(), list_element, new
                )
        else:
            self.say("did.not.found.list", list=list_element)

    def try_to_update(self, list_element, entity, new):
        list_content = List.get(list_element)
        i = list_content.index(entity)
        list_content[i] = new
        List.save(list_element, list_content, "w")
        self.say(
            "changed.item",
            entity=entity.title(),
            list=list_element.title(),
            new=new.title()
        )

    def add_new(self, responce: bool, list_element: str, new: str):
        list_element = list_element.lower()
        entity = new.lower()
        if responce:
            List.append(list_element, entity)
            self.say("added.item", entity=entity.title(), list=list_element.title())
        else:
            self.say("cancel.adding", entity=entity.title(), list=list_element.title())
