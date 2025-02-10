from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from core.ai.ai import AI
from core.config import LIB_RESOURCE_PATH
from core.interface.base import BaseInterface
from core.security.key import AlexKey

class Server(BaseInterface):
    name = "server"

    def __init__(self, alex: AI):
        super().__init__(alex)
        self.socketio = None
        self.app = None

    def start(self):
        self.app = Flask(
            __name__, template_folder=f'{LIB_RESOURCE_PATH}/web/templates',
            static_folder=f'{LIB_RESOURCE_PATH}/web/static'
            )
        self.app.config['SECRET_KEY'] = str(AlexKey.get())
        self.socketio = SocketIO(self.app)

        self.socketio.on('send_message')(self.input)
        self.socketio.on('wake')(self.wakeword)
        self.socketio.on('change_mode')(self.change_mode)
        self.socketio.on('connect_user')(self.user_connect)
        self.app.add_url_rule('/', view_func=self.index)
        print(f"Running on http://{self.config['host']}:{self.config['port']}/")
        self.socketio.run(
            self.app, host=self.config["host"], port=int(self.config["port"]), log_output=False,
            )
        super().start()

    @staticmethod
    def index():
        return render_template('index.html')
    
    def close(self):
        self.socketio.stop()

    def speak(self, data):
        if data['value'] != "":
            emit('receive_message', data, broadcast=True)
