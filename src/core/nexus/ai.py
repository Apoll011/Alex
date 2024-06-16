from core.system.config import path
from core.system.context import ContextManager


class AiBluePrintSkeleton:
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

    __context = ContextManager()

    done_init_actions = False

    def __init__(self, sig) -> None:
        with open(f"{path}/core/nexus/{sig}/sys.sg", "r") as name:
            self.name = name.read()

    def activate(self):
        self.header()
        for action in self.init_actions:
            print("Running", action)
            self.init_actions[action](action, self)
        
        while not self.done_init_actions and len(self.init_actions) != 0:
            pass
        
        self.footer()
        self.start()

    def header(self):
        #os.system("clear")
        print("-"*30, "Initing", self.name, "-"*30)
    
    def footer(self):
        print("-"*30, "End initializing", self.name, "-"*30)

    def start(self):
        pass

    def deactivate(self):
        pass

    def get_context(self, name, type = "memory"):
        return self.__context.load(name, type)
    
    def register_blueprint(self, blueprint: AiBluePrintSkeleton):
        self.init_actions = blueprint.init_actions | self.init_actions
    
    def set_context(self, name, value, type = "memory"):
        self.__context.save(value, name, type)

    def finish_and_set(self, name, ctx_name, ctx_value):
        self.set_context(ctx_name, ctx_value)
        self.finish(name)

    def finish(self, name):
        self.init_actions_done.append(name)
        print("OK.....", name)
        if len(self.init_actions_done) == len(self.init_actions.keys()):
            self.done_init_actions = True
