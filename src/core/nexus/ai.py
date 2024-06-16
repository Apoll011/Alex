from core.system.config import path
from core.system.context import ContextManager
import os

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

    def header(self):
        """
        Prints a header message
        """
        print("-"*30, "Initing", self.name, "-"*30)

    def footer(self):
        """
        Prints a footer message
        """
        print("-"*30, "End initializing", self.name, "-"*30)

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
        print("OK.....", name)
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

class AI(AiRepresentatorInScreen, AiBluePrintUser):
    """
    The main AI class
    """
    def __init_subclass__(cls) -> None:
        """
        Saves the AI class instance in the context
        """
        cls._context.save(cls, cls.__name__)

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
        for action in self.init_actions:
            print("Running", action)
            self.init_actions[action](action, self)
        
        while not self.done_init_actions and len(self.init_actions) != 0:
            pass
        
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
        for action in self.deactivate_actions:
            print("Running", action)
            self.deactivate_actions[action](action, self)
        
        while not self.done_init_actions and len(self.init_actions) != 0:
            pass
        self.__end()
