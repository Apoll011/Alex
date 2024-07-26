from pydub import AudioSegment
from pydub.playback import play
from core.resources.data_files import *
from core.config import path

#TODO: Change this. Instead of using 3d party modules use the API of the Inerfaces in the acton "play_audio"
class Sound:
    def __init__(self) -> None:
        pass
    
    def play_dot(self, n = "01"):
        song = AudioSegment.from_wav(DataFile.load("dot_"+n, "wav"))
        play(song)
