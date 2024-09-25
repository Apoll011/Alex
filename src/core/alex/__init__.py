import sys

from core.ai.ai import AI
from core.date import get_time_of_day
from core.error import *
from core.intents.responce import *
from core.interface.base import BaseInterface
from core.sysinformation import Registries
from .functions import alexSkeleton
from ..scheduler import Scheduler
from ..sysinformation import SysInfo

class ALEX(AI):
    mode: str

    voice_mode: bool

    next_on_loop = None
    next_on_loop_args = None

    def __init__(self) -> None:

        super().__init__("ALEX")
        self.text_processor = None
        self.register_blueprint(alexSkeleton)

        self.voice_mode = False

        self.scheduler = Scheduler()
        self.scheduler.start_scheduler()

        self.information = SysInfo()


    def interface_on(self):
        self.register_scheduled_funcs()

    def set_language(self, lang="en"):
        self.language = lang
        self.translationSystem = TranslationSystem(self.language)

    def start(self):
        self.screen.clear()

    def loop(self):
        if self.next_on_loop is not None:
            if self.next_on_loop_args:
                self.next_on_loop()
            else:
                self.next_on_loop(*self.next_on_loop_args)
            self.next_on_loop = None
            self.next_on_loop_args = None

    def speak(self, data, voice_command=None):
        if BaseInterface.is_set():
            dataP = {
                "type": "say",
                "value": data["message"],
                "settings": {
                    "intent": data["intent"],
                    "voice": data["voice"],
                    "voice_command": voice_command,
                    "voice_mode": self.voice_mode | False
                }
            }
            BaseInterface.get().process(dataP)
        else:
            raise InterfaceNotRegistered()

    def wake(self, data):
        data = {
            "type": "play_audio",
            "value": f"acknowledge.mp3",
            "settings": {
            }
        }
        BaseInterface.get().process(data)
        self.information.register(Registries.WAKE_UP)

    def end(self):
        time_of_day = self.translate(f"time.day.{get_time_of_day()}")
        self.speak(self.make_responce(self.translate("system.close", {"time_of_day": time_of_day})))
        sys.exit(0)

    def make_responce(self, message="", intent=None) -> dict[str, Any]:
        """
        Make a responce spoke by the interface just instance without any args will be an empty responce
        that won't be spoked by the interface.
        """
        if intent is None:
            intent = {}
        return {"message": message, "intent": intent, "voice": "Alex"}

    def process(self, text):
        responce = self.text_processor.process(text)
        self.speak(responce)

    def on_next_loop(self, action, *args):
        self.next_on_loop = action
        self.next_on_loop_args = args
