from core.system.interface.voice import Voice
from core.system.intents import IntentResponse
from core.system.interface.base import BaseInterface


class ComandLine(BaseInterface):
    def speak(self, data: dict[str, str | IntentResponse], voice: str = 'Alex', voice_command = None, voice_mode = False):
        print(f"{voice}: {data['message']}")

        if voice_mode:
            Voice().speak(data, voice, voice_command, False)
    
    def loop(self):
        self.input({"message": input("Your request: ")})
