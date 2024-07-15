import os

DEFALUT_LANG = "en"

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
