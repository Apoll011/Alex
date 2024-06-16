from core.system.config import path
from core.system.context import ContextManager
import os
import shutil
import threading

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
        terminal_size = shutil.get_terminal_size().columns
        border_size = (terminal_size - len(self.name) - 10 - self.name.count(" ")) // 3  # 10 is for "Initing " and spaces
        print("\33[91m-" * border_size, "\33[36mIniting", self.name,"\33[91m", "-" * border_size, "\33[97m")

    def footer(self):
        """
        Prints a footer message
        """
        terminal_size = shutil.get_terminal_size().columns
        border_size = (terminal_size - len(self.name) - 18 - self.name.count(" ")) // 3  # 14 is for "End initializing " and spaces
        print("\33[91m-" * border_size, "\33[96mEnd initializing", self.name, "\33[91m", "-" * border_size, "\33[97m")

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

    def get_context(self, name: str, type: str = "memory"):
        """
        Retrieves a context value

        Args:
            name (str): The name of the context value
            type (str): The type of the context value (default: "memory")

        Returns:
            The context value
        """
        return self._context.load(name, type)

    def set_context(self, name: str, value, type: str = "memory"):
        """
        Sets a context value

        Args:
            name (str): The name of the context value
            value: The value to be set
            type (str): The type of the context value (default: "memory")
        """
        self._context.save(value, name, type)

class AiBluePrintUser(AiContextUser):
    """
    A class to manage AI blueprints and their actions
    """
    init_actions = {
        
    }
    """
    Dictionary to store init actions
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
        self.set_context(ctx_name, ctx_value)
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

    def __init_subclass__(cls) -> None:
        """
        Registers the AI subclass in the nexus
        """
        if cls.__name__ != "Ai":
            with Nexus._lock:
                Nexus._registry[cls.__name__] = cls

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

class AI(Nexus, AiRepresentatorInScreen, AiBluePrintUser):
    """
    The main AI class
    """

    def __init__(self, sig: str) -> None:
        """
        Initializes the AI instance

        Args:
            sig (str): The signature of the AI
        """
        with open(f"{path}/core/nexus/{sig}/sys.sg", "r") as name:
            self.name = name.read()

    def activate(self):
        """
        Activates the AI instance
        """
        self.header()
        self.run_init_actions()
        
        self.footer()
        self.__start()

    def __start(self):
        """
        Starts the AI instance (not implemented)
        """
        pass

    def __end(self):
        """
        Ends the AI instance (not implemented)
        """
        pass

    def deactivate(self):
        """
        Deactivates the AI instance
        """
        self.run_deactivate_actions()
        self.__end()
