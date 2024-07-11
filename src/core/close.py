import os
from .config import path

class CloseAlex():
    temps_dirs = ["temp", "var"]

    def __init__(self) -> None:
        self.delet_temps_dir()
    
    def delet_temps_dir(self):
        for tt in self.temps_dirs:
            for f in os.listdir(path + "/data/"+tt):
                os.remove(path + "/data/"+tt + "/"+ f)