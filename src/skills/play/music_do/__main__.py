from core.system.skills.call import SkillCaller
from core.system.intents.slots import SlotValue
from core.system.skills import BaseSkill
from core.system.config import path
import os

class MusicDo(BaseSkill):
     def __init__(self):
          self.register("play@music.do")
          super().__init__()

     def execute(self, context, intent):
          super().execute(context, intent)
          self.optional("musicDo", SlotValue)
          self.optional("musicTrackAction", SlotValue)
          self.optional("musicReapeatOptions", SlotValue)
          self.optional("shuffleEnabled", SlotValue)


          if self.slots["musicDo"]:
                self.comand(self.slots["musicDo"].value)
          if self.slots["musicTrackAction"]:
                self.comand(self.slots["musicTrackAction"].value + " track")
          if self.slots["musicReapeatOptions"]:
                self.comand(f"Set song repeat to {self.slots["musicReapeatOptions"].value}")
          if self.slots["shuffleEnabled"]:
                self.comand(f"Set shuffle enabled to {self.slots["shuffleEnabled"].value.replace("\\", "")}")
          
          self.responce_translated("Ok") # type: ignore
     
     def comand(self, text):
               os.system(f"zsh \"{path}/skills/play/np.sh\" do \"{text}\"")
          
     def responce(self, text):
          self.speak(text)
