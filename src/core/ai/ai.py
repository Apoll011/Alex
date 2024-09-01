import sys
import time
from typing import Any
from .dna import AlexDna
from core.config import path
from .scheduler import Scheduler
from .translate import Translator
from .context import AiContextUser
from core.api.client import ApiClient
from .blueprint import AiBluePrintUser
from .internetuser import InternetUser
from .screen import AiRepresentatorInScreen

class AI(AlexDna, AiBluePrintUser, AiContextUser, Translator, AiRepresentatorInScreen, InternetUser, Scheduler):
    """
    The main AI class
    """

    api: ApiClient
    active: bool

    sig: str

    debug_mode = False

    database: dict

    language: str

    base_server_ip: str = "127.0.0.1"


    def __init__(self, sig: str) -> None:
        """
        Initializes the AI instance

        Args:
            sig (str): The signature of the AI
        """
        with open(f"{path}/core/{sig}/sys.sg", "r") as name:
            self.name = name.read()
        
        self.done_init_actions = False

        self.sig = sig

    def activate(self):
        """
        Activates the AI instance
        """
        self.clear()
        self.header()
        self.run_init_actions()
        
        self.active = True
        if not self.debug_mode:
            time.sleep(0.1)
        self.footer()

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

    def interface_on(self): ...
    def process(self, message) -> dict[str, Any]: ...
    def wake(self, data): ...
    def on_next_loop(self, callback): ...
    def speak(self, data, voice_command = None): ...
