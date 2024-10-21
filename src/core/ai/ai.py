import sys
import time
from typing import Any

from core.client import ApiClient
from core.dna import DNA
from .blueprint import AiBluePrintUser
from ..context import ContextManager
from ..notifier import Notify
from ..scheduler import Scheduler
from ..screen import Screen

class AI(
    AiBluePrintUser
    ):
    """
    The main Activation Instance class
    """

    api: ApiClient
    active: bool

    sig: str

    debug_mode = False

    database: dict

    language: str

    base_server_ip: str = "127.0.0.1"

    language: str

    context = ContextManager()
    """
    The context manager
    """

    notifier: Notify = Notify()
    def __init__(self, sig: str) -> None:
        """
        Initializes the AI instance

        Args:
            sig (str): The signature of the AI
        """

        self.scheduler: Scheduler | None = None
        self.dna = DNA()
        self.screen = Screen(sig)

        self.translationSystem = None

        self.name = "ALEX"
        
        self.done_init_actions = False

        self.sig = sig

    def activate(self):
        """
        Activates the AI instance
        """
        self.screen.clear()
        self.screen.header()
        self.run_init_actions()
        
        self.active = True
        if not self.debug_mode:
            time.sleep(0.1)
        self.screen.footer()

    def start(self):
        """
        Starts the AI instance
        """
        

    def end(self):
        """
        Ends the AI instance
        """
        sys.exit(1)

    def deactivate(self):
        """
        Deactivates the AI instance
        """
        self.run_deactivate_actions()
        self.end()

    def loop(self):
        """
        Will Always loop over unless `active` is set to `False` 
        """

    def handle_request(self, request, *args, **kwargs):
        if request in self.request_actions.keys():
            return self.request_actions[request](self, *args, **kwargs)
        else:
            raise ValueError(f"AI request '{request}' not found")

    def translate(self, key: str, context: dict[str, Any] | None = None, return_none=False):
        return self.translationSystem.get_translation(key, context, return_none)

    def translate_responce(self, key: str, context: dict[str, Any] | None = None, intent=None, voice=None):
        if intent is None:
            intent = {}
        return self.make_responce(self.translate(key, context), intent, voice)

    def get_context(self, name: str, type: str = "pickle"):
        """
        Retrieves a context value

        Args:
            name (str): The name of the context value
            type (str): The type of the context value (default: "pickle")

        Returns:
            The context value
        """
        return self.context.load(name, type)

    def set_context(self, name: str, value, type: str = "pickle"):
        """
        Sets a context value

        Args:
            name (str): The name of the context value
            value: The value to be set
            type (str): The type of the context value (default: "pickle")
        """
        self.context.save(value, name, type)

    def make_responce(self, message="", intent=None, voice=None) -> dict[str, Any]:
        ...
    def interface_on(self): ...
    def process(self, message) -> dict[str, Any]: ...
    def wake(self, data): ...
    def on_next_loop(self, callback): ...
    def speak(self, data, voice_command = None): ...
