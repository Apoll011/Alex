from flask_cors import CORS, cross_origin
from core.system.config import path
from core.system.ai.nexus import Nexus
from flask import Flask, render_template, make_response
from flask_socketio import SocketIO, emit
from core.system.security._key import AlexKey
from core.system.interface.voice import Voice
from core.system.intents import IntentResponse
from core.system.interface.base import BaseInterface

class Server(BaseInterface):
    def start(self):
        self.app = Flask(__name__, template_folder=f'{path}/resources/templates', static_folder=f'{path}/resources/static')
        CORS(self.app, resources={r"/music": {"origins": "http:/127.0.0.1:5855/"}})
        self.app.config['SECRET_KEY'] = str(AlexKey.get())
        self.socketio = SocketIO(self.app)

        self.socketio.on('send_message')(self.input)
        self.socketio.on('wake')(self.wakeword)
        self.socketio.on('change_mode')(self.change_mode)
        self.socketio.on('conect')(self.user_conect)
        self.app.add_url_rule('/', view_func=self.index)
        self.socketio.run(self.app, host="0.0.0.0", port=80) # type: ignore

    def index(self):
        responce = make_response(render_template('index.html'))
        responce.headers.add('Access-Control-Allow-Origin', '*')
        return responce
    
    def close(self):
        self.socketio.stop()

    def speak(self, data: dict[str, str | IntentResponse], voice: str = 'Alex', voice_command = None, voice_mode = False):
        emit('receive_message', {'message': data['message'], 'intent': data['intent'], 'ai': voice}, broadcast=True) # type: ignore
        if voice_mode:
            Voice().speak(data, voice, voice_command, False)
