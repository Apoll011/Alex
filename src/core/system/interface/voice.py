import os
import subprocess
from core.system.config import path
from core.system.ai.nexus import Nexus
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

    voice_file_path = "./src/resources/data/temp/alex_speak.m4a"

    say_voice_command = "say -v '{name}' '{text}' -o {vfp} --data-format=alac"

    def start(self):
        self.user_conect({})

    def speak(self, data: dict[str, str | IntentResponse], voice: str = 'Alex', voice_command = None, voice_mode = False):
        if voice_command is None:
            command = self.say_voice_command
        else:
            command = voice_command

        command = command.format(name=voice, text=data["message"], vfp=self.voice_file_path) # type: ignore

        os.system(command)

        ALEX = Nexus.get_ai("ALEX")
        ALEX.interface.send_audio(f"{path}/{self.voice_file_path}") # type: ignore

    def listen(self):
        print("Listening...")
        c = "hear -m -p -t 2"
        result = subprocess.check_output(c, shell=True, text=True)
        return result
