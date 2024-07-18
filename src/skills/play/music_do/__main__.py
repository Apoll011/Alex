import os
from core.config import path
from core.skills import BaseSkill

class MusicDo(BaseSkill):
     def init(self):
          self.register("play@music.do")
          self.save_responce_for_context = False
          self.can_go_again = False

     def execute(self, context, intent):
          super().execute(context, intent)
          self.optional("musicDo")
          self.optional("musicTrackAction")
          self.optional("musicReapeatOptions")
          self.optional("shuffleEnabled")


          if self.slot_exists("musicDo"):
                self.comand(self.slots["musicDo"].value)
          if self.slot_exists("musicTrackAction"):
                self.comand(self.slots["musicTrackAction"].value + " track")
          if self.slot_exists("musicReapeatOptions"):
                self.comand(f"Set song repeat to {self.slots["musicReapeatOptions"].value}")
          if self.slot_exists("shuffleEnabled"):
                self.comand(f"Set shuffle enabled to {self.slots["shuffleEnabled"].value.replace("\\", "")}")
          
          self.responce_translated("Ok") # type: ignore
     
     def comand(self, text):
          os.system(f"zsh \"{path}/skills/play/np.sh\" do \"{text}\"")
