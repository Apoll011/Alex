import os
from typing import Any

from pydub import AudioSegment
from pydub.playback import play
from pydub.utils import which

from core.config import LIB_RESOURCE_PATH
from core.log import LOG

# TODO: Change this. Instead of using 3d party modules use the API of the Interfaces in the action "play_audio"
class Audio:
    audio_handle = {
        "mp3": AudioSegment.from_mp3,
        "raw": AudioSegment.from_raw,
        "wav": AudioSegment.from_wav,
        "ogg": AudioSegment.from_ogg,
        "flv": AudioSegment.from_flv
    }

    @staticmethod
    def check():
        if which("avconv") or which("ffmpeg"):
            return True
        return False

    @staticmethod
    def play(audio_name):
        audio_path = Audio.get_path(audio_name)
        if Audio.check():
            song = Audio.get_handler(audio_name)(audio_path)
            play(song)
        else:
            os.system(f"aplay {audio_path}")

    @staticmethod
    def get_handler(audio_name) -> (Any, dict[str, Any]):
        extension = audio_name.split(".")
        try:
            return Audio.audio_handle[extension]
        except KeyError:
            LOG.error(f"The audio extension {extension} is not supported.")
            raise AudioExtensionNotSupported(audio_name)

    @staticmethod
    def get_path(audio_name):
        if os.path.isfile(
                audio_name
        ):  # FIXME: Used for skill sound playing. But imagine the user puts another file with the name "dot_01.mp3" in the same path as alex...
            return audio_name

        path = f"{LIB_RESOURCE_PATH}/audio/{audio_name}"
        return path

    def play_dot(self, n="01"):
        self.play(f"dot_{n}.wav")

class AudioExtensionNotSupported(Exception):
    def __init__(self, audio_name):
        super().__init__(f"The audio extension on file {audio_name} is not supported.")
