from .config import path
from random import choice
import re

class TranslationSystem:
    """
    A translation system that loads translations from files and provides a way to retrieve them.

    Attributes:
        lang (str): The language code (e.g. "en", "pt", etc.)
        file (str): The file name (e.g. "system", "game", etc.)
        translations (dict): A dictionary of translations, where keys are translation keys and values are translated strings
    """

    def __init__(self, lang: str, file: str = "system", path_file = "/resources/language/") -> None:
        """
        Initializes the translation system.

        Args:
            lang (str): The language code (e.g. "en", "pt", etc.)
            file (str): The file name (e.g. "system", "game", etc.)
        """
        self.lang = lang
        self.file = file
        self.language_path = path + "/"+ path_file
        self.translations = self.load_translations()
        self.translations.update({"error.457": "The key {} was not found in this translation file map: ("+self.language_path+")"})

    def load_translations(self) -> dict[str, str | list]:
        """
        Loads translations from a file.

        Returns:
            dict: A dictionary of translations, where keys are translation keys and values are translated strings
        """
        file_path = f"{self.language_path}/{self.file}.{self.lang}.lang"
        with open(file_path, "r", encoding="UTF-8") as f:
            translations = {}
            for line in f:
                if line.strip() and line != "":
                    key, value = line.strip().split(":", 1)
                    if value.strip().startswith("["):
                        v = value.replace("[", "").replace("]", "")
                        v = re.sub(r'\{\{+\s*(.*?)\s*\}\}+', r'{\1}', v.strip())
                        translations[key] = v.split(";")
                    else:
                        translations[key] = re.sub(r'\{\{+\s*(.*?)\s*\}\}+', r'{\1}',value.strip())
            return translations

    def get_translation(self, key: str, context=None) -> str:
        """
        Retrieves a translation for a given key.

        Args:
            key (str): The translation key
            context (dict): Optional arguments to format the translation string

        Returns:
            str: The translated string
        """
        context = context or {}
        try:
            translation = self.translations[key]
            if isinstance(translation, list):
                translation = choice(translation)
            return translation.format(**context)
        
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
