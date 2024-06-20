import os

__lang__ = "pt"
__version__ = "0.7.2-BETA"


path = os.path.realpath(os.path.dirname(os.path.realpath("")) + "/Alex/src")

nexus_ai = ["WEC", "LIS", "HIS", "ALEX", "PRIA"]

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
