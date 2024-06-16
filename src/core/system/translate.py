# translation_system.py
from .config import path

class TranslationSystem:
    """
    A translation system that loads translations from files and provides a way to retrieve them.

    Attributes:
        lang (str): The language code (e.g. "en", "pt", etc.)
        file (str): The file name (e.g. "system", "game", etc.)
        translations (dict): A dictionary of translations, where keys are translation keys and values are translated strings
    """

    def __init__(self, lang: str, file: str = "system") -> None:
        """
        Initializes the translation system.

        Args:
            lang (str): The language code (e.g. "en", "pt", etc.)
            file (str): The file name (e.g. "system", "game", etc.)
        """
        self.lang = lang
        self.file = file
        self.translations = self.load_translations()

    def load_translations(self) -> dict:
        """
        Loads translations from a file.

        Returns:
            dict: A dictionary of translations, where keys are translation keys and values are translated strings
        """
        file_path = f"{path}/resources/language/{self.lang}/tradutor/{self.file}.lang"
        with open(file_path, "r", encoding="UTF-8") as f:
            translations = {}
            for line in f:
                if line.strip():
                    key, value = line.strip().split(":", 1)
                    translations[key] = value.strip().replace("#%", "{}")
            return translations

    def get_translation(self, key: str, *args) -> str:
        """
        Retrieves a translation for a given key.

        Args:
            key (str): The translation key
            *args: Optional arguments to format the translation string

        Returns:
            str: The translated string
        """
        try:
            translation = self.translations[key]
            if args:
                return translation.format(*args)
            return translation
        except KeyError:
            return self.get_translation("error.457", key)

    def __call__(self, key: str, *args) -> str:
        """
        Convenience method to retrieve a translation.

        Args:
            key (str): The translation key
            *args: Optional arguments to format the translation string

        Returns:
            str: The translated string
        """
        return self.get_translation(key, *args)
