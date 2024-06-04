import os

__lang__ = "pt"


path = os.path.realpath(os.path.dirname(os.path.realpath("")) + "/Alex/src")


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
