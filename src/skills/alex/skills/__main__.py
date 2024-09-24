import os

from core.config import SOURCE_DIR
from core.skills import BaseSkill

class Skills(BaseSkill):
    def init(self):
        self.register("alex@skills")

    def execute(self, intent):
        super().execute(intent)
        self.require("major_skill")
        self.optional("minor_skill")

        if not self.slot_exists("minor_skill"):
            self.look_for_major(self.respond_based_on_minors)
        else:
            self.look_for_major(self.respond_based_on_minor)

    def look_for_major(self, func):
        major_list = os.listdir(SOURCE_DIR + "/skills/")
        if self.assert_in("major_skill", major_list):
            func()
        else:
            self.responce_translated("not.found")

    def respond_based_on_minors(self):
        minors = self.get_minor(self.slots["major_skill"].value)
        if len(minors) == 0:
            self.responce_translated("yes.avaliable", {"major": self.slots["major_skill"], "minor": minors[0]})
        else:
            self.responce_translated(
                "yes.avaliables", {"major": self.slots["major_skill"], "minors": self.format(minors)}
            )

    def respond_based_on_minor(self):
        minors = self.get_minor(self.slots["major_skill"].value)
        if self.assert_in("minor_skill", minors):
            self.responce_translated(
                "yes.avaliable.one", {"major": self.slots["major_skill"], "minor": self.slots["minor_skill"]}
            )
        else:
            self.responce_translated("not.found")

    @staticmethod
    def get_minor(major):
        l = map(
            lambda x: " ".join(x.split("_")),
            list(
                filter(
                    lambda obj: os.path.isdir(SOURCE_DIR + "/skills/" + major + "/" + obj),
                    os.listdir(SOURCE_DIR + "/skills/" + major + "/")
                )
            )
        )
        l = list(l)
        try:
            l.remove("  pycache  ")
        except ValueError:
            pass

        return l

    @staticmethod
    def format(word_list: list):
        return ", ".join(word_list)
