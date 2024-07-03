from core.system.ai.nexus import Nexus
from core.system.intents import IntentResponse

class BaseInterface:
    def init(self):
        self.start()

    def start(self): ...
    
    def speak(self, data: dict[str, str | IntentResponse], voice: str = 'Alex', voice_command = None, voice_mode = False): ...
    
    def input(self, data): 
        message = data['message']
        retrive_message, intent = Nexus.call_ai("ALEX", "process", message)
        try: 
            new_data = {
                "intent": intent,
                "voice": "Alex"
            } | retrive_message
            self.speak(new_data)
        except TypeError:
            pass

    def wakeword(self, data):
        Nexus.call_ai("ALEX", "wake", data)
    
    def parse(self, data): ...
    
    def execute(self, comand): ...

    def loop(self): ...

    def close(self): ...

    def user_conect(self, data): ...
    
    def change_mode(self, data: dict):
        Nexus.request_ai("ALEX", "changeMode", data["mode"])
