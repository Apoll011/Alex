from core.system.ai.ai import AI
from .functions import priaSkeleton
import time

class PRIA(AI):
    def __init__(self) -> None:
        super().__init__("PRIA")
        self.register_blueprint(priaSkeleton)
        
    def start(self):
        #time.sleep(2)
        print("Booting up Alex...")
        #time.sleep(1)
        self.call_ai("ALEX", "start")
