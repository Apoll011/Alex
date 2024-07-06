import threading
from .library import *
from flask_cors import CORS
from core.system.ai.ai import AI
from .functions import mimSkeleton
from core.system.config import path
from flask import Flask, send_file, render_template

class MIM(AI):
    library: Library
    def __init__(self) -> None:
        super().__init__("MIM")
        self.library = Library()
        self.register_blueprint(mimSkeleton)

    def start(self):
        threading.Thread(target=self.start_thereaded, args=()).start()

    def start_thereaded(self):
        self.app = Flask(__name__, template_folder=f'{path}/resources/templates/music', static_folder=f'{path}/resources/static/music')
        CORS(self.app)
        self.app.config['SECRET_KEY'] = str("AlexKey.get()")
        
        self.app.add_url_rule('/music/<artist>/<name>', view_func=self.music)
        self.app.add_url_rule('/music/cover/<artist>/<name>', view_func=self.music_cover)
        self.app.add_url_rule('/', view_func=self.index)
        self.app.run(host="0.0.0.0", port=5855) # type: ignore

    def index(self):
        return render_template("index.html")

    def music(self, artist, name):
        music_result = self.library.search(name.replace("_", " "))
        for music in music_result:
            if music.match(artist, QueryMusicType.ARTIST):
                result:MusicObject = music
        return send_file(result.get_path())

    def music_cover(self, artist, name):
        return send_file("/Users/Pegasus/Library/Mobile Documents/com~apple~CloudDocs/Pegasus/Projects/Alex/Alex/src/resources/static/music/Home.jpg")
