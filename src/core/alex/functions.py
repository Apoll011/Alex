import glob
import pickle
import time
from datetime import datetime, timedelta

from core.ai.ai import AI
from core.ai.blueprint import AiBluePrintSkeleton
from core.audio import decrease_volume, increase_volume
from core.client import ApiClient
from core.codebase_managemet.base_server import get_base_server_on_local_net, is_base_server
from core.codebase_managemet.updater import AlexUpdater, AutoUpdater
from core.config import *
from core.config import EventPriority
from core.context import ContextManager
from core.error import *
from core.hardware.esp32.animation_config import ChaseConfig, GradientConfig, ProgressConfig, PulseConfig, \
    SparkleConfig, \
    StatusConfig, WaveConfig
from core.hardware.esp32.controller import ESP32BluetoothClient
from core.hardware.esp32.structures import AnimationType, Button, Pattern, PredefinedColor
from core.interface.base import BaseInterface
from core.log import LOG
from core.models import ReminderObject
from core.notifier import AlexEvent
from core.process import Process
from core.resources.application import Application
from core.resources.data_files import DataFile
from core.users.users import PersonsDB

alexSkeleton = AiBluePrintSkeleton()

server_trys = 0

@alexSkeleton.init_action("Import Alex DNA")
def dna(self, alex: AI):
    app_dna = Application.get("dna")
    alex.dna.load_dna(app_dna)
    alex.finish(self)

@alexSkeleton.init_action("Creating Context Variables")
def make_ctx(self, alex: AI):
    alex.set_context("allowed_to_check_api", True)
    alex.set_context("firstActivationCalled", False)
    alex.finish(self)

@alexSkeleton.init_action("Set Api connection")
def set_api_con(self, alex: AI):
    if alex.base_server_ip == config_file["api"]["host"] and not is_base_server(config_file["api"]["host"]):
        print(
            f"The base server is not set on the default ip {config_file["api"]["host"]} searching for the base server... \nThis process should take around {255 * API_SEARCH_TIMEOUT:0.2f} seconds"
        )
        alex.base_server_ip = get_base_server_on_local_net() or alex.base_server_ip

    try:
        LOG.info("Connecting to Base Api")
        alex.api = ApiClient(alex.base_server_ip, api['port'])
        alex.finish(self)
        return
    except ConnectionRefusedError:
        LOG.error("Base Api Closed.")
        alex.set_context("allowed_to_check_api", False)
        say("server.closed", alex)
        alex.deactivate()

@alexSkeleton.init_action("Connect to Device")
def device_con(self, alex: AI):
    alex.box_controller = ESP32BluetoothClient()
    if not alex.ignore_box:
        if not alex.box_controller.scan_and_connect():
            print("\33[31mCould not connect to device!")
    else:
        print("\33[33mSkipping connection to device!")
    alex.finish(self)

@alexSkeleton.init_action("Register Button Presses")
def r_buttons(self, alex: AI):
    for (button, func) in alex.button_pressed_func.items():
        alex.box_controller.button_handler.register_callback(button, func)
    alex.finish(self)

@alexSkeleton.init_action("Set Text Processor")
def set_api_con(self, alex: AI):
    alex.text_processor = Process(
        alex
    )
    alex.finish(self)

@alexSkeleton.init_action("Getting all Persons")
def get_persons(self, alex: AI):
    alex.persons = PersonsDB()
    alex.finish(self)

@alexSkeleton.init_action("Get Master User")
def get_master_user(self, alex: AI):
    u = alex.persons.get_from_name("Tiago")
    alex.finish_and_set(self, "master", u)

@alexSkeleton.init_action("Getting intents engine")
def train_intents(self, alex: AI):
    alex.api.call_route("intent_recognition/engine", {"lang": alex.language})
    alex.finish(self)

@alexSkeleton.init_action("Getting dictionary engine")
def load_dictionary(self, alex: AI):
    alex.api.call_route("dictionary/load", {"lang": "en"}) #TODO: Change this this to alex.language
    alex.finish(self)

@alexSkeleton.init_action("Scheduling System tasks")
def load_dictionary(self, alex: AI):
    updater = AutoUpdater()
    updater.schedule(alex)
    alex.finish(self)

@alexSkeleton.request_action("debugMode")
def debug_mode(alex: AI):
    LOG.info("Alex set ot Debug Mode")
    alex.debug_mode = True
    alex.text_processor.debug_mode = True

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
                say("server.reconnect", alex)
            if server_trys > MAXSERVER_ACCEPTED_TRYS:
                LOG.error("Server. Closed. Closing system")
                alex.set_context(
                    "allowed_to_check_api", False
                )  # This has
                # to happen since while alex is speaking, the schedule thread
                # seems to continue executing this function causing it to loop forever.
                say(f"server.reconnection.exceeded", alex, {"limit": MAXSERVER_ACCEPTED_TRYS})
                say("server.closed.exceeded", alex)
                alex.on_next_loop(alex.deactivate)
            else:
                time.sleep(SERVER_RECONNECT_DELAY.value)
                LOG.info("Trying to reconnect")
                server_trys += 1

@alexSkeleton.request_action("checkUpdates")
def check_for_updates(alex: AI):
    updater = AlexUpdater(alex)
    updater.run_update_process()

def say(key, alex: AI, context=None, voice=None):
    if context is None:
        context = {}
    alex.speak(alex.translate_responce(key, context, voice))

@alexSkeleton.request_action("sendToApi")
def sendApi(alex: AI, route: str, value=None):
    if value is None:
        value = {}
    return alex.api.call_route(route, value)

@alexSkeleton.request_action("userConnect")
def userConnect(alex: AI):
    m = alex.translate_responce(
        "system.welcome", {"user": alex.get_context("master").name}, fallback="Welcome {user}"
        )  # type: ignore
    alex.speak(m)  # type: ignore
    alex.handle_request("checkUpdates")

@alexSkeleton.request_action("changeMode")
def changeMode(alex: AI, mode):
    LOG.info(f"changed alex mode to {mode}")
    if mode == "Text":
        alex.voice_mode = False # type: ignore
    else:
        alex.voice_mode = True # type: ignore

def seconds_to_next(hour):
    now = datetime.now()
    next_occurrence = now.replace(hour=hour, minute=0, second=0)

    if now > next_occurrence:
        next_occurrence += timedelta(days=1)

    return (next_occurrence - now).seconds

@alexSkeleton.on(AlexEvent.ALEX_GOOD_MORNING)
def run_morning_actions(event, alex: AI):
    alex.set_context("firstActivationCalled", True)
    alex.scheduler.schedule(seconds_to_next(4), EventPriority.SYSTEM, alex.set_context, "firstActivationCalled", False)
    # TODO: Add ability to create morning routines

@alexSkeleton.deactivate_action("Closing Scheduler")
def stop_scheduler(alex: AI):
    LOG.info("Closing Scheduler")
    alex.scheduler.stop_scheduler(True)

@alexSkeleton.deactivate_action("Delete context")
def delete_ctx(alex: AI):
    LOG.info("Deleting the context")
    ContextManager.clear()
    files = glob.glob(f'{USER_RESOURCE_PATH}/ctx/*.pickle')
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

@alexSkeleton.deactivate_action("Disconnect to Device")
def device_desconect(alex: AI):
    if alex.box_controller:
        alex.box_controller.close()

@alexSkeleton.scheduled(5, EventPriority.SKILLS, False)
def get_reminders(alex: AI):
    LOG.info("Loading Reminders")
    reminder_list = os.listdir(DataFile.getBasePath("reminder"))
    for reminder_file in reminder_list:
        with open(DataFile.getPath(reminder_file.split(".")[0], "reminder"), "rb") as file:
            reminder: ReminderObject = pickle.load(file)
            reminder.schedule(alex)
            LOG.info(f"Reminder of ID: {reminder.id} scheduled")

@alexSkeleton.button_pressed(Button.BUTTON_VOL_PLUS)
def inc_volume(alex: AI, state):
    current_volume = increase_volume(maxv=200)
    alex.box_controller.animation_controller.play_animation(
        AnimationType.PROGRESS_INDICATOR, 2500, ProgressConfig(
            progress=current_volume if current_volume <= 100 else current_volume - 100,
            active_color=PredefinedColor.WHITE if current_volume <= 100 else PredefinedColor.RED,
            inactive_color=PredefinedColor.BLACK if current_volume <= 100 else PredefinedColor.GOLD,
        )
    )

@alexSkeleton.button_pressed(Button.BUTTON_VOL_MINUS)
def dec_volume(alex: AI, state):
    current_volume = decrease_volume()
    alex.box_controller.animation_controller.play_animation(
        AnimationType.PROGRESS_INDICATOR, 2500, ProgressConfig(
            progress=current_volume if current_volume <= 100 else current_volume - 100,
            active_color=PredefinedColor.WHITE if current_volume <= 100 else PredefinedColor.RED,
            inactive_color=PredefinedColor.BLACK if current_volume <= 100 else PredefinedColor.GOLD,
        )
    )

state = {
    "mode": 0,
    "recording": False,
    "muted": False
}

import subprocess

def get_media_status():
    """
    Gets the status of the current media (Playing, Paused, or Stopped).
    Returns:
        str: The status of the media player.
    """
    try:
        status = subprocess.check_output(["playerctl", "status"], text=True).strip()
        return status
    except subprocess.CalledProcessError:
        return "No player is running or no media available."

def get_media_info():
    """
    Gets the current media's artist and title in a formatted string.
    Returns:
        str: Formatted string with artist and title, or an error message.
    """
    try:
        metadata = subprocess.check_output(
            ["playerctl", "metadata", "--format", "{{artist}} - {{title}}"],
            text=True
        ).strip()
        return metadata
    except subprocess.CalledProcessError:
        return "No media playing or metadata unavailable."

@alexSkeleton.button_pressed(Button.BUTTON_PLAY)
def play_button_pressed(alex: AI, b_state):
    """
        Toggles play/pause on the current media player.
        Returns:
            str: A message indicating the action performed.
        """
    try:
        subprocess.run(["playerctl", "play-pause"], check=True)
        status = get_media_status()
        if status == "Playing":
            alex.box_controller.animation_controller.play_animation(
                AnimationType.CONFIGURABLE_GRADIENT,
                2000,
                GradientConfig(
                    speed=5,
                    spread=15,
                    start_hue=60,
                    reverse=False
                )
            )
        elif status == "Paused":
            alex.box_controller.animation_controller.play_animation(
                AnimationType.CONFIGURABLE_CHASE,
                2500,
                ChaseConfig(
                    fade=0,
                    tail=2,
                    color=PredefinedColor.GOLD,
                )
            )
        elif status == "No player is running or no media available.":
            alex.box_controller.animation_controller.play_animation(
                AnimationType.STATUS_INDICATOR,
                2500,
                StatusConfig(
                    blink=True,
                    pattern=Pattern.GRADIENT,
                    color=PredefinedColor.RED,
                )
            )
        return "Toggled play/pause."
    except subprocess.CalledProcessError:
        return "Failed to toggle play/pause. No media player available."

@alexSkeleton.button_pressed(Button.BUTTON_SET)
def set_button_pressed(alex: AI, b_state):
    """Play an animation based on the current mode and toggle the mode."""
    # Cycle through modes (0, 1, 2, ...)
    state["mode"] = (state["mode"] + 1) % 4
    time = 5000
    if state["mode"] == 0:
        config = PulseConfig(speed=3, min_bright=30, max_bright=255, color=PredefinedColor.BLUE)
        animation_type = AnimationType.CONFIGURABLE_PULSE
    elif state["mode"] == 1:
        config = SparkleConfig(fade=10, chance=50, color=PredefinedColor.GREEN)
        animation_type = AnimationType.CONFIGURABLE_SPARKLE
    elif state["mode"] == 2:
        config = None
        time = -1
        animation_type = AnimationType.VOICE_RESPONSE
    else:
        config = WaveConfig(speed=4, waves=3, color=PredefinedColor.RED)
        animation_type = AnimationType.CONFIGURABLE_WAVE

    alex.box_controller.animation_controller.play_animation(animation_type, time, config)

@alexSkeleton.button_pressed(Button.BUTTON_MODE)
def mode_button_pressed(alex: AI, b_state):
    """Toggle mute state and play corresponding animation."""
    state["muted"] = not state["muted"]  # Toggle mute state

    if state["muted"]:
        alex.box_controller.animation_controller.play_animation(
            AnimationType.STATUS_INDICATOR,
            2000,
            StatusConfig(
                color=PredefinedColor.RED,
                pattern=Pattern.SOLID,
                blink=True,
                bspeed=2
            )
        )
    else:
        # Unmuted state animation
        alex.box_controller.animation_controller.play_animation(
            AnimationType.STATUS_INDICATOR,
            2000,
            StatusConfig(
                color=PredefinedColor.BLUE,
                pattern=Pattern.SOLID,
                blink=True,
                bspeed=2
            )
        )

@alexSkeleton.button_pressed(Button.BUTTON_REC)
def rec_button_pressed(alex: AI, b_state):
    """Toggle recording state and play a corresponding animation."""
    state["recording"] = not state["recording"]
    if not state["recording"]:
        config = ChaseConfig(
            fade=0,
            tail=2,
            color=PredefinedColor.RED,
        )
        animation_type = AnimationType.CONFIGURABLE_CHASE
    else:
        config = StatusConfig(
            color=PredefinedColor.GREEN,
            pattern=Pattern.SOLID,
            blink=True,
            bspeed=3
        )
        animation_type = AnimationType.STATUS_INDICATOR

    alex.box_controller.animation_controller.play_animation(animation_type, 3000, config)
