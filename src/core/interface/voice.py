import os
import threading

from precise_runner import PreciseEngine, PreciseRunner

from core.ai.ai import AI
from core.config import RESOURCE_FOLDER
from core.interface.base import BaseInterface

class Voice(BaseInterface):
    
    name = "voice"
    
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

    replacers = {
        "Alex": "Alex",
        "Ema": "Karen"
    }
    
    alex_voice: str

    say_voice_command = "say -v '#name#' '#text#'"

    voice_command_extensions = ""

    allowed_after_wake_word_listen = True

    def __init__(self, alex: AI):
        super().__init__(alex)

        engine = PreciseEngine('precise', f'{RESOURCE_FOLDER}/model/model.pb')
        runner = PreciseRunner(engine, on_activation=self.wakeword, sensitivity=0.5)
        runner.start()
    
    @staticmethod
    def select_voice():
        lang = BaseInterface.get().alex.language
        preference = Voice.alex_voice_preference[lang]
        return Voice.alex_possibilities[lang][preference]

    def start(self):
        self.user_connect({})
        self.voice_command_extensions = "--interactive=/cyan"
        super().start()

    def on_wake_word(self):
        self.allowed_after_wake_word_listen = False
        self.waiting_for_message = True
        message = self.listen(2)
        self.waiting_for_message = False
        if not message.strip() == "":
            print(f"{self.request_sentence}: \33[32m {message} \33[0m")
            self.input({"message": message})   
            self.allowed_after_wake_word_listen = True
            threading.Thread(target=self.after_wake_word).start()
        else:
            print("NULL MESSAGE")

    def speak(self, data):
        if data['value'] != "":
            #Voice.s(data, f" {self.voice_command_extensions}")
            print(data['value'])
        
    @staticmethod
    def s(data, extension = ""):

        if data["settings"]["voice_command"] is None:
            command = Voice.say_voice_command
        else:
            command = data["settings"]["voice_command"]

        command += extension

        voice = Voice.replacers[data["settings"]["voice"]]

        if voice == "Alex":
            voice = Voice.select_voice()
        
        command = command.replace('#name#', voice).replace('#text#', data['value']) # type: ignore

        os.system(command)

    def listen(self, timeout: int):
        """ c = f"hear -p -t {timeout}"
        result = subprocess.check_output(c, shell=True, text=True)
        return result.strip().split("\n")[-1].strip().lstrip().rstrip() """
        return input("Input: ")

    def after_wake_word(self):
        if self.allowed_after_wake_word_listen:
            print("Listening for continuation...")
            self.on_wake_word()
            print("Ended listening of continuation")
        else:
            self.allowed_after_wake_word_listen = True
