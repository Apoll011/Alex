import os
from core.config import path
from core.skills import BaseSkill

class Music(BaseSkill):
	def init(self):
		self.register("play@music")
		self.save_responce_for_context = False
		self.can_go_again = False

	def execute(self, context, intent):
		super().execute(context, intent)
		self.optional("artist")
		self.optional("track")
		self.optional("album")
		self.optional("genre")

		if len(self.slots) == 0:
			os.system(f"zsh \"{path}/skills/play/np.sh\" do playpause")
			return
		
		flag = "-l"
		pattern = ""
		if self.slot_exists("artist"):
			pattern = self.slots["artist"].value
			flag = "-a"

		if self.slot_exists("track"):
			pattern = self.slots["track"].value
			flag = "-s"

		if self.slot_exists("album"):
			pattern = self.slots["album"].value
			flag = "-p"

		if self.slot_exists("genre"):
			pattern = self.slots["genre"].value
			flag = "-g"

		self.comand(flag, pattern)
		self.responce_translated("Ok")
     
	def comand(self, flag, pattern):
		os.system(f"zsh \"{path}/skills/play/np.sh\" play {flag} \"{pattern}\"")
