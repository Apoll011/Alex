from typing import Any

from pydub import AudioSegment
from pydub.playback import play

from core.config import LIB_RESOURCE_PATH

# TODO: Change this. Instead of using 3d party modules use the API of the Interfaces in the action "play_audio"
class Audio:
    audio_handle = {
        "mp3": AudioSegment.from_mp3,
        "raw": AudioSegment.from_raw,
        "wav": AudioSegment.from_wav,
        "ogg": AudioSegment.from_ogg,
        "flv": AudioSegment.from_flv
    }

    def play(self, audio_name):
        song = self.get_handler(audio_name)(self.get_path(audio_name))
        play(song)

    def get_handler(self, audio_name) -> (Any, dict[str, Any]):
        extension = audio_name.split(".")
        try:
            return self.audio_handle[extension]
        except:
            raise AudioExtensionNotSupported(audio_name)

    @staticmethod
    def get_path(audio_name):
        path = f"{LIB_RESOURCE_PATH}/audio/{audio_name}"
        return path

    def play_dot(self, n="01"):
        song = AudioSegment.from_wav(self.get_path(f"dot_{n}.wav"))
        play(song)

class AudioExtensionNotSupported(Exception):
    def __init__(self, audio_name):
        super().__init__(f"The audio extension on file {audio_name} is not supported.")
