from typing import Any

from core.translate import TranslationSystem

class Responce:
    rtype: Any
    replace = {

    }
    hard_search = False

    result: Any

    translate: TranslationSystem

    default = None

    def is_accepted(self, text) -> bool:
        try:
            self.get_result(self.clear_text(text))
            return True
        except ValueError:
            return False

    def get_result(self, text):
        try:
            if len(self.replace) > 0:
                self.result = self.rtype(self.replace[self.parse(text)])
            else:
                self.result = self.rtype(self.parse(text))
        except (ValueError, KeyError, Exception):
            if self.default is not None:
                self.result = self.default
            raise ValueError

    def parse(self, text):
        if len(self.replace) > 0:
            if self.hard_search:
                return text.lower()
            else:
                for e in self.replace.keys():
                    if e in text.lower():
                        return e
        else:
            return text

    def set_translation_system(self, translation_system: TranslationSystem):
        self.translate = translation_system

    def init(self):
        ...

    @staticmethod
    def clear_text(text: str):
        new_text = text.strip()

        # TODO: REMOVE ACCENT
        return new_text

class AnyResponce(Responce):
    def is_accepted(self, text) -> bool:
        self.result = text
        return True

class SomethingFromListOrNoneResponce(Responce):

    def __init__(self, list_word) -> None:
        for e in list_word:
            self.replace.update({e: 1})
        self.list = list_word

    def is_accepted(self, text) -> bool:
        self.none_text = self.translate.get_translation("none.text").lower()
        self.replace[self.none_text] = None
        if self.none_text in text.lower():
            self.result = None
            return True

        for elem in self.list:
            if text.lower() in elem.lower():
                self.result = text
                return True

        return False

class SomethingOrNoneResponce(Responce):
    def is_accepted(self, text) -> bool:
        none_text = self.translate.get_translation("none.text").lower()
        self.result = text
        if none_text in text:
            self.result = None
        return True

class BoolResponce(Responce):
    rtype = bool

    def init(self):
        yes = self.translate.get_translation("yes.text").lower()
        no = self.translate.get_translation("no.text").lower()
        allways = self.translate.get_translation("allways.text").lower()
        never = self.translate.get_translation("never.text").lower()
        self.replace[yes] = True
        self.replace[no] = False
        self.replace[allways] = True
        self.replace[never] = False

class HardBoolResponce(Responce):
    rtype = bool

    def init(self):
        self.replace["yes"] = True
        self.replace["no"] = False
        self.replace["sim"] = True
        self.replace["nao"] = False
        self.replace["não"] = False
