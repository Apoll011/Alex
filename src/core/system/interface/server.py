from core.system.config import path
from core.system.ai.nexus import Nexus
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from core.system.security._key import AlexKey
from core.system.interface.voice import Voice
from core.system.intents import IntentResponse
from core.system.interface.base import BaseInterface

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

    def speak(self, data: dict[str, str | IntentResponse], voice: str = 'Alex', voice_command = None, voice_mode = False):
        emit('receive_message', {'message': data['message'], 'intent': data['intent'], 'ai': voice}, broadcast=True) # type: ignore
        if voice_mode:
            Voice().speak(data, voice, voice_command, False)
