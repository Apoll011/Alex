import json
import os
import pickle
from .config import path

class ContextManager:
    __contexts = {}
    __file_dir = "/resources/ctx/"

    def __enter__(self, context_name):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def save(self, obj, context_name, file_format="memory"):
        """Save an context to the contexts dictionary and optionally to a file.

        Args:
            obj (context): The context to save.
            context_name (str): The name of the context to save the context under.
            file_format (str, optional): The file format to use when saving the context to a file.
                Supported formats are "pickle" and "json". Defaults to "memory".
        """
        
        if file_format == "pickle":
            self.__save_to_file(obj, context_name, "pickle")
        elif file_format == "json":
            self.__save_to_file(obj, context_name, "json")
        elif file_format == "memory":
            self.__contexts[context_name] = obj
        else:
            raise ValueError(f"Invalid file format: {file_format}")

    @classmethod
    def load(cls, context_name, file_format="pickle"):
        """Load an context from the contexts dictionary and optionally from a file.

        Args:
            context_name (str): The name of the context to load the context from.
            file_format (str, optional): The file format to use when loading the context from a file.
                Supported formats are "pickle" and "json". Defaults to "pickle".

        Returns:
            context: The loaded context.
        """
        obj = cls.__contexts.get(context_name)
        if obj is None:
            if file_format == "pickle":
                obj = cls.__load_from_file(context_name, "pickle")
            elif file_format == "json":
                obj = cls.__load_from_file(context_name, "json")
            else:
                raise ValueError(f"Invalid file format: {file_format}")
        return obj

    def delete(self, context_name):
        """Delete an context from the contexts dictionary and optionally from a file.

        Args:
            context_name (str): The name of the context to delete the context from.
        """
        if context_name in self.__contexts:
            del self.__contexts[context_name]
        if os.path.exists(self.get_file_path(context_name, "pickle")):
            os.remove(self.get_file_path(context_name, "pickle"))
        if os.path.exists(self.get_file_path(context_name, "json")):
            os.remove(self.get_file_path(context_name, "json"))

    @staticmethod
    def __save_to_file(obj, context_name, file_format):
        """Save an context to a file.

        Args:
            obj (context): The context to save.
            context_name (str): The name of the context to use as the file name.
            file_format (str): The file format to use. Supported formats are "pickle" and "json".
        """
        if file_format == "pickle":
            with open(ContextManager.get_file_path(context_name, "pickle"), "wb") as f:
                pickle.dump(obj, f)
        elif file_format == "json":
            with open(ContextManager.get_file_path(context_name, "json"), "w") as f:
                json.dump(obj, f)

    @staticmethod
    def __load_from_file(context_name, file_format):
        """Load an context from a file.

        Args:
            context_name (str): The name of the context to use as the file name.
            file_format (str): The file format to use. Supported formats are "pickle" and "json".

        Returns:
            context: Theloaded context.
        """
        if file_format == "pickle":
            with open(ContextManager.get_file_path(context_name, "pickle"), "rb") as f:
                return pickle.load(f)
        elif file_format == "json":
            with open(ContextManager.get_file_path(context_name, "json"), "r") as f:
                return json.load(f)

    @staticmethod
    def get_file_path(context_name, file_format):
        """Get the file path for a given context name and file format.

        Args:
            context_name (str): The name of the context.
            file_format (str): The file format. Supported formats are "pickle" and "json".

        Returns:
            str: The file path.
        """
        file_name = f"{context_name}.{file_format}"
        return os.path.join(ContextManager.__file_dir, file_name)

    @classmethod
    def list_contexts(cls):
        """Get a list of all context names.

        Returns:
            list: A list of context names.
        """
        return list(cls.__contexts.keys())

    @classmethod
    def clear(cls):
        """Clear all contexts from the contexts dictionary and delete all files.

        Returns:
            None
        """
        cls.__contexts.clear()
        for file in os.listdir(cls.__file_dir):
            os.remove(os.path.join(cls.__file_dir, file))
