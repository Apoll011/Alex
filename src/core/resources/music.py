from pydub import AudioSegment
from pydub.playback import play
from core.resources.data_files import *
from core.config import path


class Sound:
    def __init__(self) -> None:
        pass
    
    def play_dot(self, n = "01"):
        song = AudioSegment.from_wav(DataFile.load("dot_"+n, "wav"))
        play(song)
