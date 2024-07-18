from core.interface.voice import Voice
from core.intents import IntentResponse
from core.interface.base import BaseInterface


class ComandLine(BaseInterface):

    def start(self):
        self.user_conect({})
        super().start()

    def speak(self, data: dict[str, str | IntentResponse], voice: str = 'Alex', voice_command = None, voice_mode = False):
        if data['message'] != "":
            if self.waiting_for_message:
                print()
                self.waiting_for_message = False
            print(f"\33[0m{voice}: \33[36m{data['message']}\33[0m")
            if voice_mode:
                Voice.s(data, voice, voice_command, False)
    
    def loop(self):
        self.waiting_for_message = True
        message = input(f"{self.request_sentence}: \33[32m")
        print("\33[0m", end="")
        self.waiting_for_message = False
        self.input({"message": message})
        