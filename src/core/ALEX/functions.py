import os
import time
import glob
import pickle
from core.log import LOG
from core.error import *
from core.ai.ai import AI
from core.config import *
from core.api.client import ApiClient
from core.config import EventPriority
from core.models import ReminderObject
from core.interface.base import BaseInterface
from core.resources.data_files import DataFile
from core.ai.blueprint import AiBluePrintSkeleton
from core.resources.application import Application


alexSkeleton = AiBluePrintSkeleton()

trainig_actions = {
    "training.intents": lambda ai: ai.api.call_route("intent_recognition/get/train")
}

server_trys = 0

@alexSkeleton.init_action("Import Alex DNA")
def dna(self, alex: AI):
    dna = Application.get("dna")
    alex.load_dna(dna)
    alex.finish(self)

@alexSkeleton.init_action("Creating important Context Variables")
def make_ctx(self, alex: AI):
    alex.set_context("allowed_to_check_api", True)
    alex.finish(self)

@alexSkeleton.init_action("Set Api conection")
def set_api_con(self, alex: AI):
    try:
        LOG.info("Conecting to Base Api")
        alex.api = ApiClient(api['host'], api['port'])
        alex.finish(self)
        return
    except ConnectionRefusedError:
        LOG.error("Base Api Closed.")
        alex.clear()
        alex.set_context("allowed_to_check_api", False)
        say("server.closed", alex)
        alex.deactivate()

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

#TODO: Change print to say.
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
    LOG.info("Alex set ot Debug Mode")
    alex.debug_mode = True

@alexSkeleton.request_action("checkApi")
@alexSkeleton.scheduled(SERVER_RECONECT_DELAY, EventPriority.ALEX)
def check_api(alex: AI):
    global server_trys
    allowed_to_check_api = alex.get_context("allowed_to_check_api")
    if allowed_to_check_api:
        LOG.info("Cheking the Api...")
        try:
            api_responce = alex.api.call_route("alex/alive")
            responce = api_responce.response

            if "on" not in responce.keys():
                raise ServerClosed()
            
            kits = responce["kit"]
            
            server_trys = 0

            if not kits["all_on"]:
                print("\33[0m")
                say("server.changed", alex)
                LOG.info("Server changed reimporting the kits")

            else:
                return

            if not kits["user"]:
                LOG.info("Loading User kit from server")
                say("server.kit.user.not.loaded", alex)
                say("server.kit.user.loaded", alex)

            if not kits["intent"]:
                LOG.info("Loading Intent recognition kit from server")
                say("server.kit.intent.not.loaded", alex)
                alex.api.call_route("intent_recognition/get/reuse")
                say("server.kit.intent.loaded", alex)
            
            if not kits["dictionary"]:
                LOG.info("Loading Dictionary kit from server")
                say("server.kit.dictionary.not.loaded", alex)
                alex.api.call_route("dictionary/load", "en") #TODO: Change this this to alex.language
                say("server.kit.dictionary.loaded", alex)

            say("server.kits.loaded", alex)
            
        except Exception:
            if server_trys == 0:
                LOG.warning("The server is Offline")
                say("server.offline", alex)
                say("server.reconect", alex)
            if server_trys > MAXSERVER_ACCEPTD_TRYS:
                LOG.error("Server. Closed. Closing system")
                alex.set_context("allowed_to_check_api", False)# This has to happen since while alex is speaching the schedule theread seems to continue executing this function causeing it too loop forever.
                say(f"server.reconection.exceded", alex, {"limit": MAXSERVER_ACCEPTD_TRYS})
                say("server.closed.exceded", alex)
                alex.on_next_loop(alex.deactivate)
            else:
                time.sleep(SERVER_RECONECT_DELAY)
                LOG.info("Trying to reconect")
                server_trys += 1
                check_api(alex)

def say(key, alex: AI, context = {}):
    alex.speak(alex.translate_responce(key, context))

@alexSkeleton.request_action("sendToApi")
def sendApi(alex: AI, route: str, value: str | dict[str, str] = ""):
    return alex.api.call_route(route, value)

@alexSkeleton.request_action("userConect")
def userConect(alex: AI):
     m = alex.translate_responce("system.welcome", {"user": alex.get_context("master")["name"]}) # type: ignore
     alex.speak(m) # type: ignore

@alexSkeleton.request_action("changeMode")
def changeMode(alex: AI, mode):
    LOG.info(f"changed alex mode to {mode}")
    if mode == "Text":
        alex.voice_mode = False # type: ignore
    else:
        alex.voice_mode = True # type: ignore
        
@alexSkeleton.deactivate_action("Closing Scheduler")
def stopt_scheduler(alex: AI):
    LOG.info("Closing Scheduler")
    alex.stopt_scheduler(True)

@alexSkeleton.deactivate_action("Delete context")
def delete_ctx(alex: AI):
    LOG.info("Deleting the context")
    files = glob.glob(f'{path}/resources/ctx/*.pickle')
    for f in files:
        os.remove(f)

@alexSkeleton.deactivate_action("Delete Temporary Files")
def delete_temp(alex: AI):
    LOG.info("Deleting the temp dir")
    for file in os.listdir(DataFile.getBasePath("temp")):
        os.remove(f"{DataFile.getBasePath("temp")}/{file}")

@alexSkeleton.deactivate_action("Closing Interface")
def close_interface(alex: AI):
    LOG.info("Closing the Alex Interface")
    BaseInterface.get().close()

@alexSkeleton.scheduled(5, EventPriority.SKILLS, False)
def get_reminders(alex: AI):
    LOG.info("Loading Reminders")
    list = os.listdir(DataFile.getBasePath("reminder"))
    for reminder_file in list:
        with open(DataFile.getPath(reminder_file.split(".")[0], "reminder"), "rb") as file:
            reminder: ReminderObject = pickle.load(file)
            reminder.schedule(alex)
            LOG.info(f"Reminder of ID: {reminder.id} scheduled")
