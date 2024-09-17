import subprocess

from core.config import path
from core.skills import BaseSkill

class WhatsPlaying(BaseSkill):
     def init(self):
          self.register("music@whats.playing")

     def execute(self, intent):
          super().execute(intent)
          name, artist, album = self.beutify(self.comand())
          return self.responce_translated("playing.now", {"artist":artist, "track":name}) # type: ignore
          
     def comand(self):
          result = subprocess.check_output(f"zsh \"{path}/skills/music/np.sh\" now", shell=True, text=True)
          return result

     def beutify(self, text):
          v = text.split("\n")
          v.pop()
          return v 
