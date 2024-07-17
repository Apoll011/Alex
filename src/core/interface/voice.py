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

    @staticmethod
    def select_voice():
        lang = BaseInterface.get().alex.language
        preference = Voice.alex_voice_preference[lang]
        return Voice.alex_possibilities[lang][preference]

    def start(self):
        self.user_conect({})
        super().start()

    def speak(self, data: dict[str, str | IntentResponse], voice: str = 'Alex', voice_command = None, voice_mode = False):
        if data['message'] != "":
            Voice.s(data, voice, voice_command, voice_mode)
        
    @staticmethod
    def s(data: dict[str, str | IntentResponse], voice: str = 'Alex', voice_command = None, voice_mode = False):

        if voice_command is None:
            command = Voice.say_voice_command
        else:
            command = voice_command

        if voice == "Alex":
            voice = Voice.select_voice()
        
        command = command.replace('#name#', voice).replace('#text#', data['message']) # type: ignore

        os.system(command)

    def listen(self):
        print("Listening...")
        c = "hear -m -p -t 2"
        result = subprocess.check_output(c, shell=True, text=True)
        return result
