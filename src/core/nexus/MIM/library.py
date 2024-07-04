import re
from glob import glob
from enum import Enum
from random import shuffle
from dataclasses import dataclass
from core.system.ai.ai import AI
from core.system.ai.nexus import Nexus

class WrongMusicTypeQuery(Exception): ...

class RepeatMode(Enum):
    NO = 0
    REPEAT_PLAYLIST = 1
    REPEAT_SONG = 2

class PlayMode(Enum):
    NORMAL = 0
    SHUFFLE = 1 

class QueryMusicType(Enum):
    NAME = 0
    ALBUM = 1
    ARTIST = 2

@dataclass
class Music:
    name: str
    album: str
    artist: str

    type: str = "mp3"

    def match(self, query:str, type: QueryMusicType):
        if query.lower() == self.get_artibute(type):
            return True
        else: 
            return False
        
    def get_artibute(self, type:QueryMusicType):
        if type == QueryMusicType.NAME:
            return self.name.lower()
        elif type == QueryMusicType.ALBUM:
            return self.album.lower()
        elif type == QueryMusicType.ARTIST:
            return self.artist.lower()
        else:
            raise WrongMusicTypeQuery(f"The type {type} is not valid.")

    def get_path(self):
        return f"/Users/Pegasus/Music/Music/Media.localized/Music/{self.artist}/{self.album}/{self.name}.{self.type}"

class Library:

    __musics: list[Music] = []

    currently: Music

    music_path = "/Users/Pegasus/Music/Music/Media.localized/Music"

    def get_music(self, path):
        name = re.sub(rf'{self.music_path}/.*?/.*?/(.*?).mp3', r'\1',path)
        album = re.sub(rf'{self.music_path}/.*?/(.*?)/.*?.mp3', r'\1',path)
        artist = re.sub(rf'{self.music_path}/(.*?)/.*?/.*?.mp3', r'\1',path)

        return Music(name, album, artist)

    def add_music(self, music: Music):
        self.__musics.append(music)

    def start_import(self):
        files = glob(f'{self.music_path}/*/*/*.mp3')
        for music in files:
            self.add_music(self.get_music(music))

    def search(self, query:str, type: QueryMusicType = QueryMusicType.NAME):
        result = []
        for m in self.__musics:
            if m.match(query, type):
                result.append(m)
        
        return result

    def get_currently_playing(self):
        return self.currently

    def play(self, music:Music):
        self.currently = music
        
        ALEX:AI = Nexus.get_ai("ALEX") # type: ignore
        ALEX.interface.send_audio(music.get_path())
    
    def get_library_size(self) -> int:
        return len(self.__musics)

    def play_list(self, music_list:list[Music], mode:PlayMode = PlayMode.NORMAL, repeat:RepeatMode = RepeatMode.NO):
        if mode == PlayMode.SHUFFLE:
            shuffle(music_list)
        
        repeat_list = True
        while repeat_list:
            repeat_list = False
            
            if repeat == RepeatMode.REPEAT_PLAYLIST:
                repeat_list = True
            
            for music in music_list:
                repeat_music = True

                while repeat_music:

                    repeat_music = False
                    if repeat == RepeatMode.REPEAT_SONG:
                        repeat_music = True

                    self.play(music)
