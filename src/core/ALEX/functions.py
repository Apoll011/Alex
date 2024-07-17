import os
import time
import glob
from core.ai.ai import AI
from core.config import *
from core.api.client import ApiClient
from core.config import EventPriority
from core.interface.base import BaseInterface
from core.ai.blueprint import AiBluePrintSkeleton
from core.resources.application import Application


alexSkeleton = AiBluePrintSkeleton()

trainig_actions = {
    "training.intents": lambda ai: ai.api.call_route("intent_recognition/get/train")
}

allowed_to_check_api = True
server_trys = 0

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

#TODO: Make this speach based on language chosen
@alexSkeleton.request_action("checkApi")
@alexSkeleton.scheduled(SERVER_RECONECT_DELAY, EventPriority.ALEX)
def check_api(alex):
    global server_trys, allowed_to_check_api
    if allowed_to_check_api:
        try:
            api_responce = alex.api.call_route("alex/alive")
            responce = api_responce.response

            if "on" not in responce.keys():
                raise ServerClosed()
            
            kits = responce["kit"]
            
            server_trys = 0

            if not kits["all_on"]:
                print("\33[0m")
                say("Detected a change in the server. Re-importing the kits. Please Wait.", alex)
            else:
                return

            if not kits["user"]:
                say("Users not loaded. Loading.", alex)

            if not kits["intent"]:
                say("Intent Recognition not loaded. Loading.", alex)
                alex.api.call_route("intent_recognition/get/reuse")
                say("Done loading Intent Recognition", alex)
            
            if not kits["dictionary"]:
                say("Dictionary not loaded. Loading.", alex)
                alex.api.call_route("dictionary/load", "en") #TODO: Change this this to alex.language
                say("Done loading Dictionary.", alex)

            say("Done, Fixing the Server. All System Online.", alex)
            
        except Exception:
            if server_trys == 0:
                say("The Server is Offline.", alex)
                say("Trying to re-connect...", alex)
            if server_trys > MAXSERVER_ACCEPTD_TRYS:
                allowed_to_check_api = False # This has to happen since while alex is speaching the schedule theread seems to continue executing this function causeing it too loop forever.
                say(f"The limit of {MAXSERVER_ACCEPTD_TRYS} reconetions failed exceded.", alex)
                say("Sorry. But the Server is closed. So I am closing myself.", alex)
                alex.on_next_loop(alex.deactivate)
            else:
                time.sleep(SERVER_RECONECT_DELAY)
                server_trys += 1
                check_api(alex)

def say(text, alex):
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
        
@alexSkeleton.deactivate_action("Closing Scheduler")
def stopt_scheduler(alex: AI):
    alex.stopt_scheduler(True)

@alexSkeleton.deactivate_action("Delete context")
def delete_ctx(alex: AI):
    files = glob.glob(f'{path}/resources/ctx/*.pickle')
    for f in files:
        os.remove(f)

@alexSkeleton.deactivate_action("Closing Interface")
def close_interface(alex: AI):
    BaseInterface.get().close()

class ServerClosed(Exception):
    def __init__(self) -> None:
        super().__init__("The Alex Base Server Is Closed.")
