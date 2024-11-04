import os

from core.skills import BaseSkill
from core.utils import resource_path

class Skills(BaseSkill):
    def init(self):
        self.register("alex@skills")
        self.dir_path = resource_path("skills/")

    def execute(self, intent):
        super().execute(intent)
        self.require("major_skill")
        self.optional("minor_skill")

        if not self.slot_exists("minor_skill"):
            self.look_for_major(self.respond_based_on_minors)
        else:
            self.look_for_major(self.respond_based_on_minor)

    def look_for_major(self, func):
        major_list = os.listdir(self.dir_path)
        if self.assert_in("major_skill", major_list):
            func()
        else:
            self.say("not.found")

    def respond_based_on_minors(self):
        minors = self.get_minor(self.get("major_skill"))
        if len(minors) == 0:
            self.say("yes.available", major=self.get("major_skill"), minor=minors[0])
        else:
            self.say(
                "yes.availables", major=self.get("major_skill"), minors=self.format(minors)
            )

    def respond_based_on_minor(self):
        minors = self.get_minor(self.get("major_skill"))
        if self.assert_in("minor_skill", minors):
            self.say(
                "yes.available.one", major=self.get("major_skill"), minor=self.get("minor_skill")
            )
        else:
            self.say("not.found")

    def get_minor(self, major):
        l = map(
            lambda x: " ".join(x.split("_")),
            list(
                filter(
                    lambda obj: os.path.isdir(self.dir_path + "/" + major + "/" + obj),
                    os.listdir(self.dir_path + "/" + major + "/")
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
