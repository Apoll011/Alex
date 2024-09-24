import os
import re
from random import choice

from core.log import LOG
from .config import DEFAULT_LANG, RESOURCE_FOLDER

class TranslationSystem:
    """
    A translation system that loads translations from files and provides a way to retrieve them.

    :var lang (str): The language code (e.g. "en", "pt", etc.)
    :var file (str): The file name (e.g. "system", "game", etc.)
    :var translations (dict): A dictionary of translations, where keys are translation keys and values are translated strings
    """

    def __init__(
            self, lang: str, file: str = "system", path_file=f"{RESOURCE_FOLDER}/language/"
    ) -> None:
        """
        Initializes the translation system.

        Args:
            lang (str): The language code (e.g. "en", "pt", etc.)
            file (str): The file name (e.g. "system", "game", etc.)
        """
        self.lang = lang
        self.file = file
        self.language_path = path_file
        self.translations = self.load_translations()
        self.translations.update(
            {"error.451": "The key {key} does not have a valid output"}
        )
        self.translations.update(
            {
                "error.457": "The key {key} was not found in this translation file map: ("
                             + self.language_path
                             + ")"
            }
        )

    def load_translations(self) -> dict[str, str | list]:
        """
        Loads translations from a file.

        :return: A dictionary of translations, where keys are translation keys and values are translated strings
        """
        file_path = f"{self.language_path}/{self.file}.{self.lang}.lang"
        if not os.path.isfile(file_path):
            file_path = f"{self.language_path}/{self.file}.{DEFAULT_LANG}.lang"

        try:
            with open(file_path, "r", encoding="UTF-8") as f:
                translations = {}
                for line in f:
                    if line.strip() and line != "":
                        key, value = line.strip().split(":", 1)
                        if value == "":
                            value = self.get_translation("error.451", {"key": key})
                        if value.strip().startswith("["):
                            v = value.replace("[", "").replace("]", "")
                            v = re.sub(r"\{\{+\s*(.*?)\s*\}\}+", r"{\1}", v.strip())
                            translations[key] = v.split(";")
                        else:
                            translations[key] = re.sub(
                                r"\{\{+\s*(.*?)\s*\}\}+", r"{\1}", value.strip()
                            )
                return translations
        except FileNotFoundError:
            LOG.error(
                f"The file {self.file}.{self.lang}.locale was not found on path {self.language_path}"
            )
            return {}

    def get_translation(self, key: str, context=None, return_none=False) -> str:
        """
        Retrieves a translation for a given key.

        :param key: The translation key
        :param context: Optional arguments to format the translation string
        :param return_none: If key is not found return None

        :return: The translated string

        :raises KeyError: If the key is not found on the dictionary and raise_error is set to True.
        """
        context = context or {}
        try:
            translation = self.translations[key]
            if isinstance(translation, list):
                translation = choice(translation)
            return translation.format(**context)

        except KeyError:
            LOG.warning(
                f"The Key {key} was not found in {self.file}.{self.lang}.locale on path {self.language_path}"
            )
            return self.get_translation("error.457", {"key": key}) if not return_none else None

    def __call__(self, key: str, *args) -> str:
        """
        Convenience method to retrieve a translation.
        :param key: The translation key
        :param args: Optional arguments to format the translation string

        :return: The translated string
        """
        return self.get_translation(key, *args)
