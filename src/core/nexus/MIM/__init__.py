import threading
from .library import *
from .functions import mimSkeleton
from core.system.ai.ai import AI
from flask import Flask, send_file

class MIM(AI):
    library: Library
    def __init__(self) -> None:
        super().__init__("MIM")
        self.library = Library()
        self.register_blueprint(mimSkeleton)

    def start(self):
        threading.Thread(target=self.start_thereaded, args=()).start()

    def start_thereaded(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = str("AlexKey.get()")
        
        self.app.add_url_rule('/music/<artist>/<name>', view_func=self.music)
        self.app.run(host="0.0.0.0", port=5855) # type: ignore

    def music(self, artist, name):
        music_result = self.library.search(name.replace("_", " "))
        for music in music_result:
            if music.match(artist, QueryMusicType.ARTIST):
                result:MusicObject = music
        return send_file(result.get_path())
