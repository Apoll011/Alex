from playsound import playsound
from .data_files import *
from ..config import path


class Sound:
    def __init__(self) -> None:
        pass
    
    def play_dot(self, n = "01"):
        playsound(DataFile.load("dot_"+n, "wav"))