import time
import sys
from .nexus import Nexus
from flask_socketio import emit
from .chatserver import ChatServer
from .context import AiContextUser
from core.system.config import path
from .blueprint import AiBluePrintUser
from .internetuser import InternetUser
from .screen import AiRepresentatorInScreen
from core.system.api.client import ApiClient



class AI(Nexus, AiBluePrintUser, AiContextUser, AiRepresentatorInScreen, ChatServer, InternetUser):
    """
    The main AI class
    """

    api: ApiClient
    active: bool


    debug_mode = False

    def __init__(self, sig: str) -> None:
        """
        Initializes the AI instance

        Args:
            sig (str): The signature of the AI
        """
        with open(f"{path}/core/nexus/{sig}/sys.sg", "r") as name:
            self.name = name.read()
        self.register_ai(sig, self)

        self.done_init_actions = False

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
        while self.active:
            self.loop()

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
