from core.system.intents.slots import SlotValue
from core.system.skills import BaseSkill
from core.system.config import path
import os

class Music(BaseSkill):
	def __init__(self):
		self.register("play@music")
		super().__init__()

	def execute(self, context, intent):
		super().execute(context, intent)
		self.optional("artist", SlotValue)
		self.optional("track", SlotValue)
		self.optional("album", SlotValue)
		self.optional("genre", SlotValue)
		
		flag = "-l"
		pattern = ""
		if self.slots["artist"]:
			pattern = self.slots["artist"].value
			flag = "-a"
		if self.slots["track"]:
			pattern = self.slots["track"].value
			flag = "-s"
		if self.slots["album"]:
			pattern = self.slots["album"].value
			flag = "-p"
		if self.slots["genre"]:
			pattern = self.slots["genre"].value
			flag = "-g"
		self.comand(flag, pattern)
		self.responce_translated("Ok") # type: ignore
     
	def comand(self, flag, pattern):
		os.system(f"zsh \"{path}/skills/play/np.sh\" play \"{flag}\" \"{pattern}\"")
          
	def responce(self, text):
		self.speak(text)
