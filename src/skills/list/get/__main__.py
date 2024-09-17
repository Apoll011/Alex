from core.skills import BaseSkill
from plugins.list import Lists

class Get(BaseSkill):
    def init(self):
        self.register("list@get")
        self.can_go_again = False
        self.list_obj = Lists.load()

    def execute(self, intent):
        super().execute(intent)
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
        text: str = self.list_obj.get(self.get("list"))
        self.responce(text)
