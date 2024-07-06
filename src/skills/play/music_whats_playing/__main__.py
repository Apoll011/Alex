import subprocess
from core.system.config import path
from core.system.ai.nexus import Nexus
from core.system.skills import BaseSkill


class MusicWhatsPlaying(BaseSkill):
     def __init__(self):
          self.register("play@music.whats.playing")
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          print(Nexus.request_ai("MIM", "getCurrentSong"))
          name, artist, album = self.beutify(self.comand())
          return self.responce_translated("playing.now", {"artist":artist, "track":name}) # type: ignore
          
     def comand(self):
          result = subprocess.check_output(f"zsh \"{path}/skills/play/np.sh\" now", shell=True, text=True)
          return result

     def beutify(self, text):
          v = text.split("\n")
          v.pop()
          return v 
