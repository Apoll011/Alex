from playsound import playsound
from core.system.resources.data_files import *
from core.system.config import path


class Sound:
    def __init__(self) -> None:
        pass
    
    def play_dot(self, n = "01"):
        playsound(DataFile.load("dot_"+n, "wav"))
