from core.nexus.ai import AiBluePrintSkeleton, AI
from core.system.api.call import ApiCall
import time

alexSkeleton = AiBluePrintSkeleton()

trainig_actions = {
    "training.intents": lambda ai: ai.api.call_route("intent_recognition/get/train")
}

@alexSkeleton.init_action("Set Api conection")
def set_api_con(self, alex: AI):
    alex.api = ApiCall("127.0.0.1", 1178)
    alex.finish(self)

@alexSkeleton.init_action("Geting intents engine")
def train_intents(self, alex: AI):
    promise = alex.api.call_route_async("intent_recognition/get/reuse")
    promise.then(lambda data: alex.finish(self))


@alexSkeleton.request_action("retrain")
def train_engine(alex: AI):
    alex.clear()
    time_stared = time.time()
    alex.print_header_text("Re-trainig", 2)
    print("Re-trainig everyting. This process take around 1 to 10 minutes please wait...")
    for act in trainig_actions:
        name = act.replace(".", " ").title()
        print(name)
        trainig_actions[act](alex)
        print("Ended", name)
    print("Time Took:", time.time() - time_stared)
    alex.print_header_text("Ended Re-Training")
    
