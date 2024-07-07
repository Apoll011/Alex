from .library import *
from core.system.ai.ai import AI
from core.system.ai.blueprint import AiBluePrintSkeleton

mimSkeleton = AiBluePrintSkeleton()

@mimSkeleton.init_action("Load The Music")
def load_countries(self, mim: AI):
    l:Library = mim.library # type: ignore
    l.start_import()
    mim.finish(self)

@mimSkeleton.request_action("searchSong")
def searchSong(mim: AI, songQuery: str, queryType: QueryMusicType):
    sresult = mim.library.search(songQuery, queryType) # type: ignore
    return sresult

@mimSkeleton.request_action("playSong")
def playSong(mim: AI, music: MusicObject):
    mim.library.play(music) # type: ignore
    return None

@mimSkeleton.request_action("playPause")
def playPause(mim: AI, music: MusicObject):
    alex = Nexus.get_ai("ALEX")
    alex.interface.emit("playpause", {})
    return None

@mimSkeleton.request_action("playList")
def playList(mim: AI, musicList: list[MusicObject], mode:PlayMode = PlayMode.NORMAL, repeat:RepeatMode = RepeatMode.NO):
    mim.library.play_list(musicList, mode, repeat) # type: ignore
    return None

@mimSkeleton.request_action("getCurrentSong")
def getCurrent(mim: AI):
    return mim.library.get_currently_playing() # type: ignore
