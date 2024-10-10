import threading
import time

from core.ai.ai import AI
from core.config import *
from core.log import LOG

class BaseInterface:
    closed = False
    _registry: 'BaseInterface'
    _name: str

    request_sentence: str

    waiting_for_message = False
    
    config = {}
    
    name = ""

    def __init__(self, alex: AI):
        self.responce_sentence = None
        self.alex = alex
        self.config = interfaces_config[self.name]
        self.register()
    
    def init(self):
        LOG.info(f"Started interface {self.__class__.__name__}")
        self.print_header()
        self.request_sentence = self.alex.translate("system.request")
        self.responce_sentence = self.alex.translate("system.responce")
        self.alex.interface_on()
        self.alex.start()


    def print_header(self):
        print("Starting on", self.name.title(),"interface:\33[32m", self.name,"\33[0m")
    
    def start(self):
        loop = threading.Thread(name = "MainLoop", target=self.start_loop)
        loop.start()
        while not self.closed:
            self.loop()

    def start_loop(self): 
        while not self.closed:
            time.sleep(ALEX_LOOP_DELAY)
            self.alex.loop()

    def speak(self, data): ...
    
    def input(self, data): 
        message = data['message']
        if message != "":
            message_processed = self.process_input(message)
            self.alex.process(message_processed)
        
    def wakeword(self, data = 1):
        self.alex.wake({"prob":data})
        self.on_wake_word()

    def on_wake_word(self): ...
    
    def parse(self, data): ...
    
    def execute(self, comand): ...

    def loop(self): ...

    def close(self):
        LOG.info("Deactivating Alex")
        self.closed = True
        LOG.info("Closed Alex")

    def user_connect(self, data):
        LOG.info("User Connected")
        self.alex.handle_request("userConnect")
        
    def change_mode(self, data: dict):
        self.alex.handle_request("changeMode", data["mode"])

    def register(self) -> None:
        """
        Registers the Interface
        """
        BaseInterface._registry = self
        BaseInterface._name = self.__class__.__name__

    @classmethod
    def get(cls):
        return cls._registry
    
    @classmethod
    def is_set(cls):
        if cls._registry:
            return True
        return False

    @classmethod
    def get_name(cls):
        return cls._name

    @staticmethod
    def process_input(text: str):
        text = text.strip()
        text = text.replace("×", " times ").replace("÷", " over ").replace("+", " plus ").replace("-", " minus ")
        return text

    def process(self, data):
        data_type = data["type"]

        match data_type:
            case "say":
                self.speak(data)

            case "play_audio":
                try:
                    raise NotImplementedError()
                    # Audio.play(data['value'])
                except Exception:
                    os.system(f"aplay {LIB_RESOURCE_PATH}/audio/{data['value']}")
            case _:
                raise KeyError(f"The type {data_type} is not valid")
