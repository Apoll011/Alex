import subprocess

from core.config import SOURCE_DIR
from core.skills import BaseSkill

class WhatsPlaying(BaseSkill):
    def init(self):
        self.register("music@whats.playing")

    def execute(self, intent):
        super().execute(intent)
        name, artist, album = self.beautify(self.command())
        return self.say("playing.now", artist=artist, track=name)

    @staticmethod
    def command():
        result = subprocess.check_output(f"zsh \"{SOURCE_DIR}/skills/music/np.sh\" now", shell=True, text=True)
        return result

    @staticmethod
    def beautify(text):
        v = text.split("\n")
        v.pop()
        return v
