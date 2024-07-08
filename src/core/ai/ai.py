import sys
import time
from .context import AiContextUser
from core.system.config import path
from .blueprint import AiBluePrintUser
from .internetuser import InternetUser
from .screen import AiRepresentatorInScreen
from core.system.api.client import ApiClient

class AI(AiBluePrintUser, AiContextUser, AiRepresentatorInScreen, InternetUser):
    """
    The main AI class
    """

    api: ApiClient
    active: bool

    sig: str

    debug_mode = False

    database: dict

    def __init__(self, sig: str) -> None:
        """
        Initializes the AI instance

        Args:
            sig (str): The signature of the AI
        """
        with open(f"{path}/core/system/{sig}/sys.sg", "r") as name:
            self.name = name.read()
        
        self.done_init_actions = False

        self.sig = sig

    def activate(self):
        """
        Activates the AI instance
        """
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
