from core.skills import BaseSkill
from core.config import path
import subprocess

class MusicWhatsPlaying(BaseSkill):
     def __init__(self):
          self.register("play@music.whats.playing")
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          name, artist, album = self.beutify(self.comand())
          return self.responce_translated("playing.now", {"artist":artist, "track":name}) # type: ignore
          
     def comand(self):
          result = subprocess.check_output(f"zsh \"{path}/skills/play/np.sh\" now", shell=True, text=True)
          return result

     def beutify(self, text):
          v = text.split("\n")
          v.pop()
          return v 
