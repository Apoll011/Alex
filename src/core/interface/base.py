from core.ai.ai import AI
from core.intents import IntentResponse

class BaseInterface:
    closed = False
    _registry: 'BaseInterface'

    request_sentence: str

    def __init__(self, alex: AI):
        self.alex = alex
        print("Starting on interface:\33[32m", self.__class__.__name__,"\33[0m")
        self.request_sentence = alex.translate("system.request")
        self.register()
        
    def start(self): 
        while not self.closed:
            self.loop()
    
    def speak(self, data: dict[str, str | IntentResponse], voice: str = 'Alex', voice_command = None, voice_mode = False): ...
    
    def input(self, data): 
        message = data['message']
        data = self.alex.process(message)  # type: ignore
        self.speak(data)

    def wakeword(self, data):
        self.alex.wake(data) # type: ignore
    
    def parse(self, data): ...
    
    def execute(self, comand): ...

    def loop(self): 
        self.alex.loop()

    def close(self): 
        self.closed = True
        self.alex.deactivate()

    def user_conect(self, data):
        self.alex.handle_request("userConect")
        
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
    def get_name(cls):
        return cls._name
