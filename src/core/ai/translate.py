from typing import Any
from core.config import path
from core.translate import TranslationSystem

class Translator:
    def init_translator(self, language = "en"):
        self.translationSystem = TranslationSystem(language)

    def translate(self, key: str, context: dict[str, Any] | None = None):
        return self.translationSystem.get_translation(key, context)

    def translate_responce(self, key: str, context: dict[str, Any] | None = None, intent: dict = {}):
        return self.make_responce(self.translate(key, context), intent)
    
    def make_responce(self, message = "", intent = {}) -> dict[str, Any]: ...
