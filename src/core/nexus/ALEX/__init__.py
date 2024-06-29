import time
import http.client as httplib
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from core.nexus.ai import AI
from core.system.config import path
from .functions import alexSkeleton
from core.system.skills.call import SkillCaller
from core.system.intents import IntentParserToObject

class ChatServer:
    def init_server(self):
        self.app = Flask(__name__, template_folder=f'{path}/resources/templates', static_folder=f'{path}/resources/static')
        self.app.config['SECRET_KEY'] = 'ufi75egf68vj6u8f'
        self.socketio = SocketIO(self.app)

    def process_message(self, message):
        return f"Processed message: {message}"

    def index(self):
        return render_template('index.html')

    def handle_send_message(self, data):
        message = data['message']
        self.process_message(message)

    def start_server(self):
        self.socketio.on('send_message')(self.handle_send_message)
        self.app.add_url_rule('/', view_func=self.index)
        self.socketio.run(self.app) # type: ignore


class ALEX(AI, ChatServer):

    internet_is_on: bool

    server_mode: bool

    def __init__(self) -> None:
        super().__init__("ALEX")
        self.register_blueprint(alexSkeleton)
        self.internet_is_on = False
        self.server_mode = False
        self.intent = IntentParserToObject()            

    def start(self):
        self.clear()
        print("Hi", self.get_context("master")["name"])  # type: ignore
        if self.server_mode:
            self.start_server()
        else:
            super().start()

    def process_message(self, message):
        return self.get_text_and_process(message)

    def loop(self):
        int = self.listen()
        text_returned = self.get_text_and_process(int)
        if text_returned != None:
            self.speak(str(text_returned))

    def get_text_and_process(self, text):
        promesa = self.api.call_route("intent_recognition/parse", text)
        responce = promesa.response
        
        intent = self.intent.parser(responce)
        if intent.intent.intent_name != None:
            if self.debug_mode:
                self.intent.draw_intent(intent)
            try:
                s = SkillCaller().call(intent)
                s.execute(self._context, intent)
            except Exception as e:
                return e
        else:
            return "Sorry. Thats not a valid intent"

    def listen(self):
        if self.internet_is_on:
            time.sleep(1)
            r = super().listen().strip()
        else:
            r = input("Seu texto: ")
        if r == "":
            return self.listen()
        if self.debug_mode:
            print("Input: ", r)
        return r

    def speak(self, text: str, voice: str = 'Alex', voice_command=None):
        if self.debug_mode:
            print("Alex: ", text)
        if self.server_mode:
            emit('receive_message', {'message': text, 'username': "Alex"}, broadcast=True)
        return super().speak(text, voice, voice_command)

    def internet_on(self):
        connection = httplib.HTTPConnection("google.com",timeout=3)
        try:
            # only header requested for fast operation
            connection.request("HEAD", "/")
            connection.close()  # connection closed
            return True
        except Exception as exep:
            return False
