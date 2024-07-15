import os
import time
import glob
from core.ai.ai import AI
from core.config import api, path
from core.api.client import ApiClient
from core.config import EventPriority
from core.interface.base import BaseInterface
from core.ai.blueprint import AiBluePrintSkeleton
from core.resources.application import Application


alexSkeleton = AiBluePrintSkeleton()

trainig_actions = {
    "training.intents": lambda ai: ai.api.call_route("intent_recognition/get/train")
}

@alexSkeleton.init_action("Import Alex DNA")
def dna(self, alex: AI):
    dna = Application.get("dna")
    alex.load_dna(dna)
    alex.finish(self)

@alexSkeleton.init_action("Set Api conection")
def set_api_con(self, alex: AI):
    alex.api = ApiClient(api['host'], api['port'])
    alex.finish(self)


@alexSkeleton.init_action("Get Master User")
def get_master_user(self, alex: AI):
    p = alex.api.call_route_async("users/search/tags", {"query": "Master"})
    p.then(lambda user: alex.finish_and_set(self, "master", alex.api.call_route("users/get", user.response["users"][0]).response))

@alexSkeleton.init_action("Geting intents engine")
def train_intents(self, alex: AI):
    promise = alex.api.call_route_async("intent_recognition/get/reuse")
    promise.then(lambda data: alex.finish(self))

@alexSkeleton.init_action("Geting dictionary engine")
def load_dictionary(self, alex: AI):
    d = alex.api.call_route("dictionary/load", "en") #TODO: Change this this to alex.language
    alex.finish(self)

@alexSkeleton.init_action("Checking the Api")
def checking_The_api(self, alex: AI):
    check_api(alex)
    alex.finish(self)


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
        action = trainig_actions[act]
        print("Prossesing Request...")
        action(alex)
        alex.print_header_text("Ended " + name, 3)
    print("\33[93mTime Took:", time.time() - time_stared, "seconds")
    alex.print_header_text("Ended Re-Training", 1)

@alexSkeleton.request_action("debugMode")
def debug_mode(alex: AI):
    alex.debug_mode = True

@alexSkeleton.request_action("checkApi")
@alexSkeleton.scheduled(5, EventPriority.ALEX)
def check_api(alex: AI):
    api_responce = alex.api.call_route("alex/alive")
    responce = api_responce.response

    if "on" not in responce.keys():
        raise ServerClosed()
    
    kits = responce["kit"]
    
    if not kits["all_on"]:
        print("\33[0m")
        if alex.debug_mode:
            alex.print_header_text("Server Changed", 3)
        say_or_print_debug("Detected a change in the server re-importing the kits. Please Wait.", alex)
    else:
        return

    if not kits["user"]:
        say_or_print_debug("Users not loaded. Loading.", alex)

    if not kits["intent"]:
        say_or_print_debug("Intent not loaded. Loading.", alex)
        alex.api.call_route("intent_recognition/get/reuse")
        say_or_print_debug("Done loading Intent", alex)
    
    if not kits["dictionary"]:
        say_or_print_debug("Dictionary not loaded. Loading.", alex)
        alex.api.call_route("dictionary/load", "en") #TODO: Change this this to alex.language
        say_or_print_debug("Done loading Dictionary.", alex)

    if alex.debug_mode:
        alex.print_header_text("Done", 3)

def say_or_print_debug(text, alex):
    if alex.debug_mode:
        print(f"{text}")
    else:
        alex.speak(alex.make_responce(text))

@alexSkeleton.request_action("sendToApi")
def sendApi(alex: AI, route: str, value: str | dict[str, str] = ""):
    return alex.api.call_route(route, value)

@alexSkeleton.request_action("userConect")
def userConect(alex: AI):
     m = alex.translate_responce("system.welcome", {"user": alex.get_context("master")["name"]}) # type: ignore
     alex.speak(m) # type: ignore

@alexSkeleton.request_action("changeMode")
def changeMode(alex: AI, mode):
    if mode == "Text":
        alex.voice_mode = False # type: ignore
    else:
        alex.voice_mode = True # type: ignore
        
@alexSkeleton.deactivate_action("Delete context")
def delete_ctx(alex: AI):
    files = glob.glob(f'{path}/resources/ctx/*.pickle')
    for f in files:
        os.remove(f)

@alexSkeleton.deactivate_action("Closing Scheduler")
def stopt_scheduler(alex: AI):
    alex.stopt_scheduler()

class ServerClosed(Exception):
    def __init__(self) -> None:
        super().__init__("The Alex Base Server Is Closed.")
