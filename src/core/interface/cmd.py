from core.interface.base import BaseInterface
from core.interface.voice import Voice

class CommandLine(BaseInterface):
    name = "cmd"
    
    def start(self):
        self.user_connect({})
        super().start()

    def speak(self, data):
        if data['value'] != "":
            if self.waiting_for_message:
                print()
                self.waiting_for_message = False
            print(f"\33[0m{data['settings']['voice']}: \33[36m{data['value']}\33[0m")
            if data["settings"]["voice_mode"]:
                Voice.s(data)
    
    def loop(self):
        self.waiting_for_message = True
        message = input(f"{self.request_sentence}: \33[32m").strip()
        print("\33[0m", end="")
        self.waiting_for_message = False
        self.input({"message": message})
        super().loop()
        