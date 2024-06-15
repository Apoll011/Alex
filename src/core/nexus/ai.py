from ..system.config import path
import os


class AiInitActionBlueprint:
    init_actions = {
        
    }
    def init_action(self, name):
        def decorator(fun): 
            self.init_actions[name] = fun
            def wrapper(*args, **kwargs):
                return fun(*args, **kwargs)
            return wrapper
        return decorator

class AI:
    name: str

    init_actions = {

    }

    init_actions_done = []

    __context = {

    }

    done_init_actions = False

    def __init__(self, sig) -> None:
        with open(f"{path}/core/nexus/{sig}/sys.sg", "r") as name:
            self.name = name.read()

    def activate(self):
        self.header()
        for action in self.init_actions:
            print("Running", action)
            self.init_actions[action](self)
        
        while not self.done_init_actions:
            pass
        
        self.footer()
        self.start()

    def header(self):
        os.system("clear")
        print("-"*30, "Initing", self.name, "-"*30)
    
    def footer(self):
        print("-"*30, "End initializing", self.name, "-"*30)

    def start(self):
        pass

    def deactivate(self):
        pass

    def get_context(self, name):
        return self.__context[name]
    
    def register_blueprint(self, blueprint: AiInitActionBlueprint):
        self.init_actions = blueprint.init_actions | self.init_actions
    
    def set_context(self, name, value):
        self.__context[name] = value

    def finish_and_set(self, name, ctx_name, ctx_value):
        self.set_context(ctx_name, ctx_value)
        self.finish(name)

    def finish(self, name):
        self.init_actions_done.append(name)
        print("OK.....", name)
        if len(self.init_actions_done) == len(self.init_actions.keys()):
            self.done_init_actions = True
