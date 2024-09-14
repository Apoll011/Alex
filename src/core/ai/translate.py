from typing import Any

from core.translate import TranslationSystem

class Translator:

    language: str

    def __init__(self):
        self.translationSystem = None

    def init_translator(self):
        self.translationSystem = TranslationSystem(self.language)

    def translate(self, key: str, context: dict[str, Any] | None = None):
        return self.translationSystem.get_translation(key, context)

    def translate_responce(self, key: str, context: dict[str, Any] | None = None, intent: dict = {}):
        return self.make_responce(self.translate(key, context), intent)
    
    def make_responce(self, message = "", intent = {}) -> dict[str, Any]: ...
