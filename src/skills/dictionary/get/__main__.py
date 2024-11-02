import re
from random import choice

from core.intents.responce import BoolResponce, SomethingFromListOrNoneResponce
from core.skills import BaseSkill
from core.utils import get_meaning_of_word

class Get(BaseSkill):
    meaning: dict
    requested: str
    def init(self):
        self.register("dictionary@get")

    def execute(self, intent):
        super().execute(intent)
        self.require("word")
        self.get_meaning(self.slots["word"].value)

    @staticmethod
    def clean(text: str):
        r = re.match("(.*)\\\\n(.Source: .*.)", text)
        if r is None:
            return text
        else:
            return r.group(1)

    def get_meaning(self, word):
        self.meaning = get_meaning_of_word(word, self.config("closest"))
        self.requested = word

        if self.meaning["name"] is None:
            self.say("not.found", word=self.requested)
            return

        if self.meaning["name"].lower() != self.requested.lower():
            self.question("not.equal", self.not_equal, {"word": self.meaning["name"]}, BoolResponce())
        else:
            self.respond_meaning()

    def not_equal(self, responce: bool):
        if responce:
            self.respond_meaning()
        else:
            others = self.meaning["others"]
            if len(others) == 0:
                self.say("not.found", word=self.requested)
            elif len(others) == 1:
                self.question(
                    "other.match", self.get_meaning_from_question, {"word": others[0]}, BoolResponce(), others[0]
                )
            else:
                self.question(
                    "other.matches", self.get_meaning_of_one_word, {"words": ", ".join(others)},
                    SomethingFromListOrNoneResponce(others)
                )

    def get_meaning_from_question(self, responce: bool, word):
        if responce:
            self.get_meaning(word)
        else:
            self.say("sorry.not.have.word")

    def get_meaning_of_one_word(self, responce: str | None):
        if responce is None:
            self.say("sorry.not.have.word")
        else:
            self.get_meaning(responce)

    def respond_meaning(self):
        if self.is_list() and len(self.meaning['definition']) > 1:
            self.respond_multiple_meaning()
        else:
            self.respond_one_meaning()

    def is_list(self):
        return isinstance(self.meaning["definition"], list)

    def respond_one_meaning(self):
        definition = self.meaning["definition"] if not self.is_list() else self.meaning["definition"][
            0]
        definition = self.clean(definition)
        self.responce(definition)

    def respond_multiple_meaning(self):
        self.question(
            "multiple.meaning", self.multiple_meaning, {"number_of_meaning": len(self.meaning['definition'])},
            BoolResponce()
        )

    def multiple_meaning(self, responce: bool):
        types_os_joins = [", and we can say that it is, ", ", or, ", ", and it is, "]
        resp = ""
        if responce:
            i = 0
            for definition in self.meaning['definition']:
                definition = self.clean(definition)
                i += 1
                if definition.endswith("."):
                    definition = definition[0:-1]
                resp += definition + f"{choice(types_os_joins) if i < len(self.meaning['definition']) else ''}"
        else:
            resp = choice(self.meaning['definition'])
        self.responce(resp)
