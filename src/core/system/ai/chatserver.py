from core.system.config import path
from flask_socketio import SocketIO
from flask import Flask, render_template
from core.system.security._key import AlexKey

class ChatServer:
    
    server_mode: bool = False

    def init_server(self):
        self.app = Flask(__name__, template_folder=f'{path}/resources/templates', static_folder=f'{path}/resources/static')
        self.app.config['SECRET_KEY'] = str(AlexKey.get())
        self.socketio = SocketIO(self.app)

    def index(self):
        return render_template('index.html')

    def handle_send_message(self, data): ...

    def change_mode(self, data: dict): ...

    def start_server(self):
        self.socketio.on('send_message')(self.handle_send_message)
        self.socketio.on('change_mode')(self.change_mode)
        self.app.add_url_rule('/', view_func=self.index)
        self.socketio.run(self.app, host="0.0.0.0", port="80") # type: ignore
