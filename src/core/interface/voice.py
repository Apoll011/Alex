import os
import subprocess
from core.intents import IntentResponse
from core.interface.base import BaseInterface

class Voice(BaseInterface):
    alex_possibilities = {
        "en": {
            "US": "Alex",
            "US2": "Fred",
            "GB": "Daniel"
        },
        "pt": {
            "PT": "Joana",
            "BR": "Luciana"
        }
    }

    alex_voice_preference = {
        "en": "US",
        "pt": "PT"
    }
    
    alex_voice: str

    say_voice_command = "say -v '#name#' '#text#'"

    voice_command_extensions = ""

    @staticmethod
    def select_voice():
        lang = BaseInterface.get().alex.language
        preference = Voice.alex_voice_preference[lang]
        return Voice.alex_possibilities[lang][preference]

    def loop(self):
        self.alex.clear()
        self.print_header()
        message = input(f"")
        if message == "":
            self.wakeword({})
            return

    def start(self):
        self.user_conect({})
        self.voice_command_extensions = "--interactive=/cyan"
        super().start()

    def on_wake_word(self):
        self.waiting_for_message = True
        try:
            message = self.listen()
            print(len(message))
            print(message, "f")
        except NotImplementedError:
            message = input(f"{self.request_sentence}: \33[32m")
            print("\33[0m")
        self.waiting_for_message = False
        self.input({"message": message})   

    def speak(self, data: dict[str, str | IntentResponse], voice: str = 'Alex', voice_command = None, voice_mode = False):
        if data['message'] != "":
            Voice.s(data, voice, voice_command, voice_mode, f" {self.voice_command_extensions}")
        
    @staticmethod
    def s(data: dict[str, str | IntentResponse], voice: str = 'Alex', voice_command = None, voice_mode = False, extension = ""):

        if voice_command is None:
            command = Voice.say_voice_command
        else:
            command = voice_command

        command += extension

        if voice == "Alex":
            voice = Voice.select_voice()
        
        command = command.replace('#name#', voice).replace('#text#', data['message']) # type: ignore

        os.system(command)

    def listen(self):
        if self.alex.debug_mode:
            print("Listening...")
            c = "hear -m -p -t 2"
            result = subprocess.check_output(c, shell=True, text=True)
            return result.strip().replace("\n", "").strip().lstrip().rstrip()
        else:
            raise NotImplementedError("Listen Function is not Implemented yet for Voice Interface")
