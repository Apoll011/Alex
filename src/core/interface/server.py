from core.config import path
from core.security._key import AlexKey
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from core.interface.base import BaseInterface

class Server(BaseInterface):
    name = "server"
    def start(self):
        self.app = Flask(__name__, template_folder=f'{path}/resources/templates', static_folder=f'{path}/resources/static')
        self.app.config['SECRET_KEY'] = str(AlexKey.get())
        self.socketio = SocketIO(self.app)

        self.socketio.on('send_message')(self.input)
        self.socketio.on('wake')(self.wakeword)
        self.socketio.on('change_mode')(self.change_mode)
        self.socketio.on('conect')(self.user_conect)
        self.app.add_url_rule('/', view_func=self.index)
        print(f"Running on http://{self.config['host']}:{self.config['port']}/")
        self.socketio.run(self.app, host=self.config["host"], port=self.config["port"])
        super().start()

    def index(self):
        return render_template('index.html')
    
    def close(self):
        self.socketio.stop()

    def speak(self, data):
        if data['value'] != "":
            emit('receive_message', data, broadcast=True)
