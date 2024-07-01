import os
import time
import shutil
import threading
import subprocess
import http.client as httplib
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from core.system.api.client import ApiClient
from core.system.security._key import AlexKey
from core.system.config import path, nexus_ai
from core.system.intents import IntentResponse
from core.system.context import ContextManager

class InternetUser:
    internet_is_on: bool

    def internet_on(self):
        connection = httplib.HTTPConnection("google.com",timeout=3)
        try:
            # only header requested for fast operation
            connection.request("HEAD", "/")
            connection.close()  # connection closed
            return True
        except Exception as exep:
            return False

class ChatServer:
    
    server_mode: bool = False

    def init_server(self):
        self.app = Flask(__name__, template_folder=f'{path}/resources/templates', static_folder=f'{path}/resources/static')
        self.app.config['SECRET_KEY'] = str(AlexKey.get())
        self.socketio = SocketIO(self.app)

    def process_message(self, message) -> (tuple[str, IntentResponse] | tuple[None, IntentResponse]): ...

    def index(self):
        return render_template('index.html')

    def handle_send_message(self, data):
        message = data['message']
        m, intent = self.process_message(message)
        if m != None:
            emit('receive_message', {'message': m}, broadcast=True)

    def change_mode(self, data: dict): ...

    def start_server(self):
        self.socketio.on('send_message')(self.handle_send_message)
        self.socketio.on('change_mode')(self.change_mode)
        self.app.add_url_rule('/', view_func=self.index)
        self.socketio.run(self.app) # type: ignore

class AiBluePrintSkeleton:
    """
    A blueprint skeleton class for AI-related actions
    """
    # Dictionary to store init actions
    init_actions = {
        
    }
    
    # Dictionary to store deactivate actions
    deactivate_actions = {
        
    }

    request_actions = {

    }

    def __init__(self) -> None:
        self.init_actions = {}
        self.deactivate_actions = {}
        self.request_actions = {}

    def init_action(self, name: str):
        """
        Decorator to register an init action

        Args:
            name (str): The name of the action

        Returns:
            A decorator function
        """
        def decorator(fun):
            self.init_actions[name] = fun
            def wrapper(*args, **kwargs):
                return fun(*args, **kwargs)
            return wrapper
        return decorator

    def deactivate_action(self, name: str):
        """
        Decorator to register a deactivate action

        Args:
            name (str): The name of the action

        Returns:
            A decorator function
        """
        def decorator(fun):
            self.deactivate_actions[name] = fun
            def wrapper(*args, **kwargs):
                return fun(*args, **kwargs)
            return wrapper
        return decorator
    
    def request_action(self, name: str):
        """
        Decorator to register a request action

        Args:
            name (str): The name of the request

        Returns:
            A decorator function
        """
        def decorator(fun):
            self.request_actions[name] = fun
            def wrapper(*args, **kwargs):
                return fun(*args, **kwargs)
            return wrapper
        return decorator
class AiSound:
    """
    A class to interact with the sound system. Plus it's still in construction so we have to use it carefully.
    """
    alex_possibilities = {
        "en_US": "Alex",
        "en_US2": "Fred",
        "en_GB": "Daniel"
    }
    
    alex_voice = alex_possibilities["en_GB"]
    pria_voice = 'Samantha'

    say_voice_command = "say -v '#name#' '#text#'"

    voice_active: bool

    def start(self) -> None:
        """
        Initializes the AiSound instance.
        """
        pass
    def listen(self):
        print("Listening...")
        c = "hear -m -p -t 2"
        result = subprocess.check_output(c, shell=True, text=True)
        return result

    def speak(self, text: str, voice: str = 'Alex', voice_command = None):
        """
        Speaks the given text using the specified voice.

        Args:
            text (str): The text to be spoken.
            voice (str): The voice to use (default: 'Alex').
            voice_command (str): The voice command to use (default: None).
        """
        command = voice_command
        if voice_command is None:
            command = self.say_voice_command
        
        command = command.replace('#name#', voice).replace('#text#', text) # type: ignore

        if self.voice_active:
            os.system(command)
        return text

class AiRepresentatorInScreen:
    """
    A class to represent AI-related information on the screen
    """
    
    name: str 
    """
        The name of the AI
    """

    def __init__(self, name: str):
        """
        Initializes the AiRepresentatorInScreen instance
        """
        self.name = name

    def header(self):
        """
        Prints a header message
        """
        self.print_header_text(f"Initializing {self.name}")

    def print_header_text(self, text, size = 2):
        s = (size + 1)
        terminal_size = shutil.get_terminal_size().columns
        border_size = (terminal_size - len(text) - 2 - self.name.count(" ")) // s  # 2 is for spaces
        print("\33[91m-" * border_size, f"\33[36m{text}\33[91m", "-" * border_size, "\33[97m")

    def footer(self):
        """
        Prints a footer message
        """
        self.print_header_text(f"End initializing {self.name}")
        
    def clear(self):
        """
        Clears the screen
        """
        os.system("clear")

class AiContextUser:
    """
    A class to manage AI-related context
    """
    
    _context = ContextManager()
    """
    The context manager
    """

    def get_context(self, name: str, type: str = "pickle"):
        """
        Retrieves a context value

        Args:
            name (str): The name of the context value
            type (str): The type of the context value (default: "pickle")

        Returns:
            The context value
        """
        return self._context.load(name, type)

    def set_context(self, name: str, value, type: str = "pickle"):
        """
        Sets a context value

        Args:
            name (str): The name of the context value
            value: The value to be set
            type (str): The type of the context value (default: "pickle")
        """
        self._context.save(value, name, type)

class AiBluePrintUser:
    """
    A class to manage AI blueprints and their actions
    """

    init_actions = {
        
    }
    """
    Dictionary to store init actions
    """

    request_actions = {

    }
    """
    Dictionary to store request actions
    """

    deactivate_actions = {
        
    }
    """
    Dictionary to store deactivate actions
    """

    init_actions_done = []
    """
        List to track completed init actions
    """

    done_init_actions = False
    """
        Flag to indicate if all init actions are completed
    """

    def finish_and_set(self, name: str, ctx_name: str, ctx_value):
        """
        Finishes an action and sets a context value

        Args:
            name (str): The name of the action
            ctx_name (str): The name of the context value
            ctx_value: The value to be set
        """
        self.set_context(ctx_name, ctx_value) # type: ignore
        self.finish(name)

    def finish(self, name: str):
        """
        Marks an action as completed

        Args:
            name (str): The name of the action
        """
        self.init_actions_done.append(name)
        print("\33[93mOK.....", name, "\33[97m")
        if len(self.init_actions_done) == len(self.init_actions.keys()):
            self.done_init_actions = True

    def register_blueprint(self, blueprint: AiBluePrintSkeleton):
        """
        Registers a blueprint and its actions

        Args:
            blueprint (AiBluePrintSkeleton): The blueprint to be registered
        """
        self.init_actions = blueprint.init_actions | self.init_actions
        self.deactivate_actions = blueprint.deactivate_actions | self.deactivate_actions
        self.request_actions = blueprint.request_actions | self.request_actions
        
    def run_init_actions(self):
        """
        Runs the registered init actions
        """
        for action in self.init_actions:
            print("\33[32mRunning", action, "\33[97m")
            self.init_actions[action](action, self)
        
        while not self.done_init_actions and len(self.init_actions) != 0:
            pass
    
    def run_deactivate_actions(self):
        for action in self.deactivate_actions:
            print("\33[32mRunning", action, "\33[97m")
            self.deactivate_actions[action](action, self)

class Nexus:
    """
    A nexus class to manage AI instances and enable communication between them
    """
    _registry = {}
    """
    Registry of AI instances
    """
    _lock = threading.RLock()
    """
    Lock for concurrent access
    """

    request_actions = {}

    def register_ai(self, name, cls) -> None:
        """
        Registers the AI subclass in the nexus
        """
        with Nexus._lock:
            Nexus._registry[name] = cls

    @classmethod
    def get_ai(cls, name: str):
        """
        Retrieves an AI instance by name

        Args:
            name (str): The name of the AI instance

        Returns:
            The AI instance
        """
        with cls._lock:
            return cls._registry.get(name)

    @classmethod
    def list_ai(cls):
        """
        Lists all registered AI instances

        Returns:
            A list of AI instance names
        """
        with cls._lock:
            return list(cls._registry.keys())

    @classmethod
    def call_ai(cls, name: str, method: str, *args, **kwargs):
        """
        Calls a method on an AI instance

        Args:
            name (str): The name of the AI instance
            method (str): The method to be called
            *args: Positional arguments for the method
            **kwargs: Keyword arguments for the method

        Returns:
            The result of the method call
        """
        ai = cls.get_ai(name)
        if ai:
            return getattr(ai, method)(*args, **kwargs)
        else:
            raise ValueError(f"AI instance '{name}' not found")

    @classmethod
    def request_ai(cls, name: str, request: str, *args, **kwargs):
        """
        Sends a request to an AI instance

        Args:
            name (str): The name of the AI instance
            request (str): The request to be sent
            *args: Positional arguments for the request
            **kwargs: Keyword arguments for the request

        Returns:
            The response from the AI instance
        """
        ai = cls.get_ai(name)
        if ai:
            return ai.handle_request(request, *args, **kwargs)
        else:
            raise ValueError(f"AI instance '{name}' not found")

    def handle_request(self, request, *args, **kwargs):
        if request in self.request_actions.keys():
            return self.request_actions[request](self, *args, **kwargs)
        else:
            raise ValueError(f"AI request '{request}' not found")

    @staticmethod
    def start_nexus():
        cm = ContextManager()
        os.system("clear")
        cm.save(False, "all_ai_started", "pickle")
        for name in nexus_ai:
            path = f"core.nexus.{name}"
            exec("from {} import {}".format(path, name))
            exec(f"{name}().activate()")
        cm.save(True, "all_ai_started", "pickle")

class AI(Nexus, AiBluePrintUser, AiContextUser, AiRepresentatorInScreen, AiSound, ChatServer, InternetUser):
    """
    The main AI class
    """

    api:ApiClient
    active: bool


    debug_mode = False

    def __init__(self, sig: str) -> None:
        """
        Initializes the AI instance

        Args:
            sig (str): The signature of the AI
        """
        with open(f"{path}/core/nexus/{sig}/sys.sg", "r") as name:
            self.name = name.read()
        self.register_ai(sig, self)

        self.done_init_actions = False

        super().start()
        

    def activate(self):
        """
        Activates the AI instance
        """
        self.header()
        self.run_init_actions()
        
        self.active = True
        if not self.debug_mode:
            time.sleep(0.1)
        self.footer()

    def start(self):
        """
        Starts the AI instance
        """
        if self.server_mode:
            self.start_server()
        else:
            while self.active:
                self.loop()

    def end(self):
        """
        Ends the AI instance (not implemented)
        """
        pass

    def deactivate(self):
        """
        Deactivates the AI instance
        """
        self.run_deactivate_actions()
        self.end()

    def loop(self):
        """
        Will Always loop over unless `active` is set to `False` 
        """

    def speak(self, text: str, voice: str = 'Alex', voice_command=None):
        if self.server_mode:
            emit('receive_message', {'message': text}, broadcast=True)
        return super().speak(text, voice, voice_command)
