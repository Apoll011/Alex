import os
from enum import Enum

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
    ONE_MINUTE = 60
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

DEFALUT_LANG = "en"

MAXSERVER_ACCEPTD_TRYS = 10
SERVER_RECONECT_DELAY = SCHEDULE_TIME.FIVE_SECONDS

ALEX_LOOP_DELAY = 1

ATENTION_WAIT_TIME = 2

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
