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
class MusicObject:
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

    __musics: list[MusicObject] = []

    currently: MusicObject

    music_path = "/Users/Pegasus/Music/Music/Media.localized/Music"

    actual_playlist: list[MusicObject]

    actual_music_pointer: int

    stop: bool = False

    def get_music(self, path):
        name = re.sub(rf'{self.music_path}/.*?/.*?/(.*?).mp3', r'\1',path)
        album = re.sub(rf'{self.music_path}/.*?/(.*?)/.*?.mp3', r'\1',path)
        artist = re.sub(rf'{self.music_path}/(.*?)/.*?/.*?.mp3', r'\1',path)

        return MusicObject(name, album, artist)

    def add_music(self, music: MusicObject):
        self.__musics.append(music)

    def start_import(self):
        files = glob(f'{self.music_path}/*/*/*.mp3')
        for music in files:
            self.add_music(self.get_music(music))

        self.actual_playlist = self.__musics
        self.actual_music_pointer = 0

    def search(self, query:str, type: QueryMusicType = QueryMusicType.NAME):
        result = []
        for m in self.__musics:
            if m.match(query, type):
                result.append(m)
        
        return result

    def get_currently_playing(self):
        return self.currently

    def play(self, music:MusicObject):
        if not self.stop:
            self.currently = music
            
            # ALEX:AI = Nexus.get_ai("ALEX") # type: ignore
            # ALEX.interface.send_audio(music.get_path())
            print(music)
    
    def start(self):
        self.stop = False

    def get_library_size(self) -> int:
        return len(self.__musics)

    def play_list(self, music_list:list[MusicObject], mode:PlayMode = PlayMode.NORMAL, repeat:RepeatMode = RepeatMode.NO):
        if mode == PlayMode.SHUFFLE:
            shuffle(music_list)
        
        self.actual_playlist = music_list
        self.actual_music_pointer = 0
        self.repeat_mode = repeat

        self.play(music_list[0])

    def next(self):
        if self.repeat_mode != RepeatMode.REPEAT_SONG:
            self.increment_pointer()
        music = self.actual_playlist[self.actual_music_pointer]
        self.play(music)

    def increment_pointer(self):
        if len(self.actual_playlist) - 1 <= self.actual_music_pointer:
            if self.repeat_mode == RepeatMode.REPEAT_PLAYLIST:
                self.actual_music_pointer = 0
            else:
                self.stop = True
        else:
            self.actual_music_pointer += 1
    
    def decrement_pointer(self):
        if self.actual_music_pointer == 0 and self.repeat_mode == RepeatMode.REPEAT_PLAYLIST:
            self.actual_music_pointer = len(self.actual_playlist)
        elif self.actual_music_pointer != 0 and self.repeat_mode != RepeatMode.REPEAT_PLAYLIST:
            self.actual_music_pointer -= 1
        else:
            self.stop = True

    def previus(self):
        self.decrement_pointer()
        music = self.actual_playlist[self.actual_music_pointer]
        self.play(music)
