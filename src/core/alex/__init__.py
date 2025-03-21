import sys

from core.ai.ai import AI
from core.error import *
from core.intents.responce import *
from core.interface.base import BaseInterface
from core.sysinformation import Registries
from core.utils import get_time_of_day
from .functions import alexSkeleton, debug_mode
from ..codebase_managemet.app import is_compiled
from ..config import BIGGEST_LOOP_ID_ALLOWED
from ..hardware.esp32.controller import ESP32BluetoothClient
from ..process import Process
from ..scheduler import Scheduler
from ..sysinformation import SysInfo

class ALEX(AI):
    mode: str

    voice_mode: bool

    next_on_loop = None
    next_on_loop_args = None
    loop_id = 0

    box_controller: ESP32BluetoothClient

    def __init__(self) -> None:

        super().__init__("ALEX")
        self.text_processor: None | Process = None
        self.register_blueprint(alexSkeleton)

        self.voice_mode = False

        self.scheduler = Scheduler()
        self.scheduler.start_scheduler()

        self.information = SysInfo()

    def interface_on(self):
        self.register_scheduled_funcs()
        self.register_notified_funcs()

    def set_language(self, lang="en"):
        self.language = lang
        self.translationSystem = TranslationSystem(self.language)

    def start(self):
        modes = []
        if not is_compiled():
            modes.append("Development Mode")
        if self.debug_mode:
            modes.append("Debug Mode")

        if len(modes) > 0:
            print("Modes:")
            for mode in modes:
                print(f"  [\33[32m{mode}\33[0m]")
    def loop(self):
        self.execute_on_next_loop()
        self.increment_loop()
        self.return_to_default_text_processor()

    def return_to_default_text_processor(self):
        if self.text_processor.id is not None and self.difference_in_loop_id(self.text_processor.id) > 20:
            self.text_processor.set_processor_on_none()
            self.text_processor.setDefaultListenProcessor()

    def execute_on_next_loop(self):
        if self.next_on_loop is not None:
            if self.next_on_loop_args:
                self.next_on_loop()
            else:
                self.next_on_loop(*self.next_on_loop_args)
            self.next_on_loop = None
            self.next_on_loop_args = None

    def increment_loop(self):
        if self.loop_id > BIGGEST_LOOP_ID_ALLOWED:
            self.loop_id = 0
        self.loop_id += 1

    def difference_in_loop_id(self, start_loop_id):
        return self.loop_id - start_loop_id if self.loop_id > start_loop_id else (
                                                                                         BIGGEST_LOOP_ID_ALLOWED + self.loop_id) - start_loop_id

    def get_loop_id(self):
        return self.loop_id

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
            "path": f"acknowledge.mp3"
        }
        BaseInterface.get().process(data)
        self.information.register(Registries.WAKE_UP)

    def end(self):
        time_of_day = self.translate(f"time.day.{get_time_of_day()}")
        translated = self.translate("system.close", {"time_of_day": time_of_day}, True)
        self.speak(self.make_responce(translated if translated else "Bye."))
        sys.exit(0)

    def make_responce(self, message="", intent=None, voice=None) -> dict[str, Any]:
        """
        Make a responce spoke by the interface just instance without any args will be an empty responce
        that won't be spoked by the interface.
        """
        if intent is None:
            intent = {}
        return {"message": message, "intent": intent, "voice": voice or "Alex"}

    def process(self, text):
        responce = self.text_processor.process(text)
        self.speak(responce)

    def on_next_loop(self, action, *args):
        self.next_on_loop = action
        self.next_on_loop_args = args