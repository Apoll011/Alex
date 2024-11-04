import os

from core.config import SOURCE_DIR
from core.skills import BaseSkill

class Play(BaseSkill):
    def init(self):
        self.register("music@play")
        self.can_go_again = False

    def execute(self, intent):
        super().execute(intent)
        self.optional("artist")
        self.optional("track")
        self.optional("album")
        self.optional("genre")

        if self.len_slots() == 0:
            os.system(f"zsh \"{SOURCE_DIR}/skills/music/np.sh\" do playpause")
            return

        flag = "-l"
        pattern = ""
        if self.slot_exists("artist"):
            pattern = self.get("artist")
            flag = "-a"

        if self.slot_exists("track"):
            pattern = self.get("track")
            flag = "-s"

        if self.slot_exists("album"):
            pattern = self.get("album")
            flag = "-p"

        if self.slot_exists("genre"):
            pattern = self.get("genre")
            flag = "-g"

        self.command(flag, pattern)
        self.say("Ok")

    @staticmethod
    def command(flag, pattern):
        os.system(f"zsh \"{SOURCE_DIR}/skills/music/np.sh\" play {flag} \"{pattern}\"")
