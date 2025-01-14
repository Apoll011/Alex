import json
import os
from enum import Enum

from core.codebase_managemet.app import home, is_compiled

class EventPriority(Enum):
    SYSTEM = 1
    ALEX = 0
    SKILLS = 2
    UI_UX = 3
    OTHERS = 4
    APPS = 3

class SCHEDULE_TIME(int, Enum):
    ONE_SECOND = 1
    FIVE_SECONDS = 5
    TEN_SECONDS = ONE_SECOND * 10
    FIFTEEN_SECONDS = ONE_SECOND * 15
    TWENTY_SECONDS = TEN_SECONDS * 2
    TWENTY_FIVE_SECONDS = ONE_SECOND * 25
    THIRTY_SECONDS = FIFTEEN_SECONDS * 2
    FORTY_SECONDS = TWENTY_SECONDS * 2
    FIFTY_SECONDS = TWENTY_FIVE_SECONDS * 2
    ONE_MINUTE = THIRTY_SECONDS * 2 
    TEN_MINUTES = ONE_MINUTE * 10
    FIFTEEN_MINUTES = ONE_MINUTE * 15
    TWENTY_MINUTES = TEN_MINUTES * 2
    TWENTY_FIVE_MINUTES = ONE_MINUTE * 25
    THIRTY_MINUTES = FIFTEEN_MINUTES * 2
    FORTY_MINUTES = TWENTY_MINUTES * 2
    FIFTY_MINUTES = TWENTY_FIVE_MINUTES * 2
    ONE_HOUR = THIRTY_MINUTES * 2
    FIVE_HOURS = ONE_HOUR * 5
    ONE_DAY = ONE_HOUR * 24

ALEX_LOOP_DELAY = 1


path = os.path.realpath("")
"""
THE base src ALEX PATH
"""

RESOURCE_FOLDER = f"{path}/resources/" if not is_compiled() else f"{home()}/.alex_resources/"
SOURCE_DIR = f"{path}/src/"

USER_RESOURCE_PATH = f"{RESOURCE_FOLDER}/user/"
LIB_RESOURCE_PATH = f"{RESOURCE_FOLDER}/lib/"

BIGGEST_LOOP_ID_ALLOWED = 1024

API_SEARCH_TIMEOUT = 0.025

try:
    with open(f"{home()}/.alex_config", "r") as config:
        config_file = json.load(config)
except FileNotFoundError:
    config_file = {
        "language": "en",
        "api": {
            "host": "127.0.0.1",
            "port": 1178,
            "max_reconnections_attempts": 10
        },
        "device": {
            "host": "192.168.1.113"
        },
        "interfaces": {
            "cmd": {},
            "voice": {},
            "server": {
                "host": "0.0.0.0",
                "port": "8416"
            },
            "api": {
                "host": "0.0.0.0",
                "port": "6752"
            }
        },
        "auto_update": {
            "allowed": True,
            "hour": "22:00"
        },
        "time_wait_after_requesting_attention": 2

    }
    with open(f"{home()}/.alex_config", "w") as config:
        json.dump(config_file, config)

API_URL = f"http://{config_file['api']['host']}:{config_file['api']['port']}/"

DEFAULT_LANG = config_file["language"]
"""
This is the default lang set a .config, It can be overwritten by the cli flag -l
"""

api = config_file["api"]
interfaces_config = config_file["interfaces"]

AUTO_UPDATE = config_file["auto_update"]["allowed"]
AUTO_UPDATE_SCHEDULED_TIME = config_file["auto_update"]["hour"]

MAXSERVER_ACCEPTED_TRYS = api["max_reconnections_attempts"]
SERVER_RECONNECT_DELAY = SCHEDULE_TIME.FIVE_SECONDS

ATTENTION_WAIT_TIME = config_file["time_wait_after_requesting_attention"]
