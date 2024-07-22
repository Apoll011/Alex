import os
import threading
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

    allowed_after_wake_word_listen = True

    @staticmethod
    def select_voice():
        lang = BaseInterface.get().alex.language
        preference = Voice.alex_voice_preference[lang]
        return Voice.alex_possibilities[lang][preference]

    def loop(self):
        message = input(f"Waiting for wake word...")
        if message == "":
            self.wakeword({})
            return

    def start(self):
        self.user_conect({})
        self.voice_command_extensions = "--interactive=/cyan"
        super().start()

    def on_wake_word(self):
        self.get_input_and_process()

    def get_input_and_process(self, timeout:int = 2):
        self.allowed_after_wake_word_listen = False
        self.waiting_for_message = True
        message = self.listen(timeout)
        self.waiting_for_message = False
        if not message.strip() == "":
            print(f"{self.request_sentence}: \33[32m {message} \33[0m")
            self.input({"message": message})   
            self.allowed_after_wake_word_listen = True
            threading.Thread(target=self.after_wake_word).start()

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

    def listen(self, timeout: int):
        c = f"hear -p -t {timeout}"
        result = subprocess.check_output(c, shell=True, text=True)
        return result.strip().split("\n")[-1].strip().lstrip().rstrip()

    def after_wake_word(self):
        if self.allowed_after_wake_word_listen:
            print("Listening for continuation...")
            self.get_input_and_process(2)
            print("Ended listening of continuation")
        else:
            self.allowed_after_wake_word_listen = True
