import glob
import pickle
import time

import psutil

from core.ai.ai import AI
from core.ai.blueprint import AiBluePrintSkeleton
from core.client import ApiClient
from core.config import *
from core.config import EventPriority
from core.error import *
from core.interface.base import BaseInterface
from core.log import LOG
from core.models import ReminderObject
from core.process import Process
from core.resources.application import Application
from core.resources.data_files import DataFile

alexSkeleton = AiBluePrintSkeleton()

training_actions = {
    "training.intents": lambda ai: ai.api.call_route("intent_recognition/engine", {"type": "train"})
}

server_trys = 0

@alexSkeleton.init_action("Import Alex DNA")
def dna(self, alex: AI):
    app_dna = Application.get("dna")
    alex.dna.load_dna(app_dna)
    alex.finish(self)

@alexSkeleton.init_action("Creating important Context Variables")
def make_ctx(self, alex: AI):
    alex.set_context("allowed_to_check_api", True)
    alex.finish(self)

@alexSkeleton.init_action("Set Api connection")
def set_api_con(self, alex: AI):
    try:
        LOG.info("Connecting to Base Api")
        alex.api = ApiClient(alex.base_server_ip, api['port'])
        alex.finish(self)
        return
    except ConnectionRefusedError:
        LOG.error("Base Api Closed.")
        alex.screen.clear()
        alex.set_context("allowed_to_check_api", False)
        say("server.closed", alex)
        alex.deactivate()

@alexSkeleton.init_action("Set Text Processor connection")
def set_api_con(self, alex: AI):
    alex.text_processor = Process(
        alex.language, alex.debug_mode, alex.api, alex.translate, alex.translate_responce, alex.make_responce
    )
    alex.finish(self)

@alexSkeleton.init_action("Get Master User")
def get_master_user(self, alex: AI):
    user = alex.api.call_route("users/search/name", {"name": "Tiago"})
    alex.finish_and_set(self, "master", alex.api.call_route("user/", {"id":user.response["users"][0]}).response)

@alexSkeleton.init_action("Getting intents engine")
def train_intents(self, alex: AI):
    alex.api.call_route("intent_recognition/engine")
    alex.finish(self)

@alexSkeleton.init_action("Getting dictionary engine")
def load_dictionary(self, alex: AI):
    alex.api.call_route("dictionary/load", {"lang": "en"}) #TODO: Change this this to alex.language
    alex.finish(self)

@alexSkeleton.request_action("retrain")
def train_engine(alex: AI):
    alex.screen.clear()
    time_stared = time.time()
    say("server.retrain", alex)
    for act in training_actions:
        name = act.replace(".", " ").title()
        say("server.retrain.thing", alex, {"name": name})
        action = training_actions[act]
        action(alex)
        say("done.text", alex)
    say("server.retrain.end", alex, {"time": time.time() - time_stared})

@alexSkeleton.request_action("debugMode")
def debug_mode(alex: AI):
    LOG.info("Alex set ot Debug Mode")
    alex.debug_mode = True

@alexSkeleton.request_action("checkApi")
@alexSkeleton.scheduled(SERVER_RECONNECT_DELAY, EventPriority.ALEX)
def check_api(alex: AI):
    global server_trys
    allowed_to_check_api = alex.get_context("allowed_to_check_api")
    if allowed_to_check_api:
        try:
            api_responce = alex.api.call_route("alex/alive")
            responce = api_responce.response

            if "on" not in responce.keys():
                raise ServerClosed()
            
            kits = responce["kit"]
            
            if not kits["all_on"] or server_trys != 0:
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
                alex.api.call_route("intent_recognition/engine")
                say("server.kit.intent.loaded", alex)
            
            if not kits["dictionary"]:
                LOG.info("Loading Dictionary kit from server")
                say("server.kit.dictionary.not.loaded", alex)
                alex.api.call_route("dictionary/load", {"lang": "en"}) #TODO: Change this this to alex.language
                say("server.kit.dictionary.loaded", alex)

            if server_trys != 0:
                server_trys = 0
                say("server.kits.loaded", alex)
            
        except Exception:
            if server_trys == 0:
                LOG.warning("The server is Offline")
                say("server.offline", alex)
                say("server.reconect", alex)
            if server_trys > MAXSERVER_ACCEPTED_TRYS:
                LOG.error("Server. Closed. Closing system")
                alex.set_context(
                    "allowed_to_check_api", False
                )  # This has
                # to happen since while alex is speaking, the schedule thread
                # seems to continue executing this function causing it to loop forever.
                say(f"server.reconection.exceded", alex, {"limit": MAXSERVER_ACCEPTED_TRYS})
                say("server.closed.exceded", alex)
                alex.on_next_loop(alex.deactivate)
            else:
                time.sleep(SERVER_RECONNECT_DELAY.value)
                LOG.info("Trying to reconnect")
                server_trys += 1

@alexSkeleton.request_action("checkApi")
@alexSkeleton.scheduled(SCHEDULE_TIME.ONE_HOUR, EventPriority.SYSTEM)
def save_sys_status(alex: AI):
    alex.system_data["cpu"].append(cpu = psutil.cpu_percent()) # type: ignore

def say(key, alex: AI, context=None):
    if context is None:
        context = {}
    alex.speak(alex.translate_responce(key, context))

@alexSkeleton.request_action("sendToApi")
def sendApi(alex: AI, route: str, value=None):
    if value is None:
        value = {}
    return alex.api.call_route(route, value)

@alexSkeleton.request_action("userConnect")
def userConnect(alex: AI):
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
def stop_scheduler(alex: AI):
    LOG.info("Closing Scheduler")
    alex.scheduler.stop_scheduler(True)

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
        os.remove(f"{DataFile.getBasePath('temp')}/{file}")

@alexSkeleton.deactivate_action("Closing Interface")
def close_interface(alex: AI):
    LOG.info("Closing the Alex Interface")
    BaseInterface.get().close()

@alexSkeleton.scheduled(5, EventPriority.SKILLS, False)
def get_reminders(alex: AI):
    LOG.info("Loading Reminders")
    reminder_list = os.listdir(DataFile.getBasePath("reminder"))
    for reminder_file in reminder_list:
        with open(DataFile.getPath(reminder_file.split(".")[0], "reminder"), "rb") as file:
            reminder: ReminderObject = pickle.load(file)
            reminder.schedule(alex)
            LOG.info(f"Reminder of ID: {reminder.id} scheduled")