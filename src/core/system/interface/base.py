import os
import subprocess
from core.system.config import path
from core.system.ai.nexus import Nexus
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from core.system.security._key import AlexKey
from core.system.intents import IntentResponse

class BaseInterface:
    def init(self):
        self.start()

    def start(self): ...
    
    def speak(self, data: dict[str, str | IntentResponse], voice: str = 'Alex', voice_command = None, voice_mode = False):
        if voice_mode:
            Voice().speak(data, voice, voice_command, False)
    
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

class ComandLine(BaseInterface):
    def speak(self, data: dict[str, str | IntentResponse], voice: str = 'Alex', voice_command = None, voice_mode = False):
        print(f"{voice}: {data['message']}")
        return super().speak(data, voice, voice_command, voice_mode)
    
    def loop(self):
        self.input({"message": input("Your request: ")})


class Server(BaseInterface):
    def start(self):
        self.app = Flask(__name__, template_folder=f'{path}/resources/templates', static_folder=f'{path}/resources/static')
        self.app.config['SECRET_KEY'] = str(AlexKey.get())
        self.socketio = SocketIO(self.app)

        self.socketio.on('send_message')(self.input)
        self.socketio.on('wake')(self.wakeword)
        self.socketio.on('change_mode')(self.change_mode)
        self.socketio.on('conect')(self.user_conect)
        self.app.add_url_rule('/', view_func=self.index)
        self.socketio.run(self.app, host="0.0.0.0", port=80) # type: ignore

    def index(self):
        return render_template('index.html')
    
    def close(self):
        self.socketio.stop()

    def user_conect(self, data):
        Nexus.request_ai("ALEX", "userConect")

    def speak(self, data: dict[str, str | IntentResponse], voice: str = 'Alex', voice_command = None, voice_mode = False):
        emit('receive_message', {'message': data['message'], 'intent': data['intent'], 'ai': voice}, broadcast=True) # type: ignore
        return super().speak(data, voice, voice_command, voice_mode)

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

        return super().speak(data, voice, voice_command, False)

    def listen(self):
        print("Listening...")
        c = "hear -m -p -t 2"
        result = subprocess.check_output(c, shell=True, text=True)
        return result
