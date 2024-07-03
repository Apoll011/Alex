import os
import subprocess
from core.system.intents import IntentResponse
from core.system.interface.base import BaseInterface

class Voice(BaseInterface):
    alex_possibilities = {
        "en_US": "Alex",
        "en_US2": "Fred",
        "en_GB": "Daniel"
    }
    
    alex_voice = alex_possibilities["en_GB"]
    pria_voice = 'Samantha'

    say_voice_command = "say -v '#name#' '#text#'"

    def speak(self, data: dict[str, str | IntentResponse], voice: str = 'Alex', voice_command = None, voice_mode = False):
        if voice_command is None:
            command = self.say_voice_command
        else:
            command = voice_command

        command = command.replace('#name#', voice).replace('#text#', data['message']) # type: ignore

        os.system(command)

    def listen(self):
        print("Listening...")
        c = "hear -m -p -t 2"
        result = subprocess.check_output(c, shell=True, text=True)
        return result
