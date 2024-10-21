from core.config import EventPriority
from core.notifier import AlexEvent

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

    scheduled_funcs = []

    notifications_events = []

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
    
    def scheduled(self, time: int, priority: EventPriority, recurring = True):
        """
        Decorator to register a schedulled event

        Args:
            time (int): Time took to execute it
            priority (int): The priority of the event lower value = Higher Priority
            recurring (bool): If event is recuring or not

        Returns:
            A decorator function
        """
        def decorator(fun):
            if recurring:
                self.scheduled_funcs.append(lambda alex: alex.scheduler.schedule_recurrent(time, priority, fun, alex))
            else:
                self.scheduled_funcs.append(lambda alex: alex.scheduler.schedule(time, priority, fun, alex))
            def wrapper(*args, **kwargs):
                return fun(*args, **kwargs)
            return wrapper

        return decorator

    def on(self, event: AlexEvent | list[AlexEvent], *args, **kwargs):
        def decorator(fun):
            self.notifications_events.append(lambda alex: alex.notifier.register(fun, event, *args, **kwargs))

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

    scheduled_funcs = []

    done_init_actions = False
    """
        Flag to indicate if all init actions are completed
    """

    notifications_events = []

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
        self.scheduled_funcs = blueprint.scheduled_funcs + self.scheduled_funcs
        self.notifications_events = blueprint.notifications_events + self.notifications_events

    def run_init_actions(self):
        """
        Runs the registered init actions
        """
        self.init_actions_done = []
        for action in self.init_actions:
            print("\33[32mRunning", action, "\33[97m")
            self.init_actions[action](action, self)
        
        while not self.done_init_actions and len(self.init_actions) != 0:
            pass
    
    def run_deactivate_actions(self):
        for action in self.deactivate_actions:
            print("\33[32mRunning", action, "\33[97m")
            self.deactivate_actions[action](self)

    def register_scheduled_funcs(self):
        for e in self.scheduled_funcs:
            e(self)

    def register_notified_funcs(self):
        for e in self.notifications_events:
            e(self)
