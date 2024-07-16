import os
from enum import Enum

class EventPriority(Enum):
    SYSTEM = 1
    ALEX = 0
    SKILLS = 2
    UI_UX = 3
    OTHERS = 4
    APPS = 3

DEFALUT_LANG = "en"

MAXSERVER_ACCEPTD_TRYS = 10
SERVER_RECONECT_DELAY = 5

path = os.path.realpath(os.path.dirname(os.path.realpath("")) + "/src")

voice: dict = {
    "voice":{
        "PRIA": {
            "en": 0,
            "pt": 2
        }, 
        "ALEX": {
            "en": 1,
            "pt": 2
        }
    },
    "speech": {
        "s": 160,
        "n": 170,
        "f": 185
    }
}

api = {
    "host": "127.0.0.1",
    "port": 1178
}
