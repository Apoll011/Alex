import os
import threading
from core.system.config import nexus_ai
from core.system.context import ContextManager

class Nexus:
    """
    A nexus class to manage AI instances and enable communication between them
    """
    _registry = {}
    """
    Registry of AI instances
    """
    _lock = threading.RLock()
    """
    Lock for concurrent access
    """

    request_actions = {}

    def register_ai(self, name, cls) -> None:
        """
        Registers the AI subclass in the nexus
        """
        with Nexus._lock:
            Nexus._registry[name] = cls

    @classmethod
    def get_ai(cls, name: str):
        """
        Retrieves an AI instance by name

        Args:
            name (str): The name of the AI instance

        Returns:
            The AI instance
        """
        with cls._lock:
            return cls._registry.get(name)

    @classmethod
    def list_ai(cls):
        """
        Lists all registered AI instances

        Returns:
            A list of AI instance names
        """
        with cls._lock:
            return list(cls._registry.keys())

    @classmethod
    def call_ai(cls, name: str, method: str, *args, **kwargs):
        """
        Calls a method on an AI instance

        Args:
            name (str): The name of the AI instance
            method (str): The method to be called
            *args: Positional arguments for the method
            **kwargs: Keyword arguments for the method

        Returns:
            The result of the method call
        """
        ai = cls.get_ai(name)
        if ai:
            return getattr(ai, method)(*args, **kwargs)
        else:
            raise ValueError(f"AI instance '{name}' not found")

    @classmethod
    def request_ai(cls, name: str, request: str, *args, **kwargs):
        """
        Sends a request to an AI instance

        Args:
            name (str): The name of the AI instance
            request (str): The request to be sent
            *args: Positional arguments for the request
            **kwargs: Keyword arguments for the request

        Returns:
            The response from the AI instance
        """
        ai = cls.get_ai(name)
        if ai:
            return ai.handle_request(request, *args, **kwargs)
        else:
            raise ValueError(f"AI instance '{name}' not found")

    def handle_request(self, request, *args, **kwargs):
        if request in self.request_actions.keys():
            return self.request_actions[request](self, *args, **kwargs)
        else:
            raise ValueError(f"AI request '{request}' not found")

    @staticmethod
    def start_nexus():
        cm = ContextManager()
        os.system("clear")
        cm.save(False, "all_ai_started", "pickle")
        for name in nexus_ai:
            path = f"core.nexus.{name}"
            exec("from {} import {}".format(path, name))
            exec(f"{name}().activate()")
        cm.save(True, "all_ai_started", "pickle")
