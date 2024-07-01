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
