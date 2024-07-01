import os
import time
import glob
from core.system.config import api, path
from core.system.api.client import ApiClient
from core.nexus.ai import AiBluePrintSkeleton, AI

alexSkeleton = AiBluePrintSkeleton()

trainig_actions = {
    "training.intents": lambda ai: ai.api.call_route("intent_recognition/get/train")
}

@alexSkeleton.init_action("Set Api conection")
def set_api_con(self, alex: AI):
    alex.api = ApiClient(api['host'], api['port'])
    alex.finish(self)

@alexSkeleton.init_action("Geting intents engine")
def train_intents(self, alex: AI):
    promise = alex.api.call_route_async("intent_recognition/get/reuse")
    promise.then(lambda data: alex.finish(self))


@alexSkeleton.request_action("retrain")
def train_engine(alex: AI):
    alex.clear()
    time_stared = time.time()
    alex.print_header_text("Re-trainig", 1)
    print("\33[34mRe-trainig everyting. This process take around 1 to 10 minutes please wait...\33[0m")
    for act in trainig_actions:
        name = act.replace(".", " ").title()
        alex.print_header_text(name, 3)
        print("Sending Request...")
        trainig_actions[act](alex)
        print("Prossesing Request...")
        alex.print_header_text("Ended " + name, 3)
    print("\33[93mTime Took:", time.time() - time_stared, "seconds")
    alex.print_header_text("Ended Re-Training", 1)

@alexSkeleton.request_action("debugMode")
def debug_mode(alex: AI):
    alex.debug_mode = True

@alexSkeleton.request_action("serverMode")
def server_mode(alex: AI):
    alex.server_mode = True
    alex.voice_active = not alex.server_mode
    alex.init_server()

@alexSkeleton.request_action("changeMode")
def changeMode(alex: AI, mode):
    if mode == "Text":
        alex.voice_active = False
    else:
        alex.voice_active = True
        
@alexSkeleton.deactivate_action("Delete context")
def delete_ctx(alex: AI):
    files = glob.glob(f'{path}/resources/ctx/*.pickle')
    for f in files:
        os.remove(f)
