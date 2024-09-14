import os
import pickle
from random import Random, randint

from .data_files import DataFile

class TemporaryFileBaseClass(DataFile):
    
    name: str
    """The file Name. Without the EXTENSION"""
    extension:str
    """File extension. Without the DOT"""

    fileBuffer = None
    """The file buffer."""


    def __init__(self, ext) -> None:
        self.path = None
        self.extension = ext

    def create(self):
        """Make a Temp File"""
        self.path = DataFile.load(self.name, self.extension, False)
        self.fileBuffer = open(self.path, "a", encoding='utf8')
        self.close()

    def write(self, data):
        """Write on the file."""
        with open(self.path, "wb") as fp:
            pickle.dump(data, fp)

    def read(self):
        """Read the temp file"""
        with open(self.path, 'rb') as fp:
            da = pickle.load(fp)
            return da

    def close(self):
        """Close the file buffer."""
        if self.fileBuffer is not None:
            self.fileBuffer.close()

    def deleteFile(self):
        """Delete the Temporary file"""
        os.remove(self.path)
        
class TemporaryFile(TemporaryFileBaseClass):
    
    def __init__(self, data:str) -> None:
        """Files for saving session data."""
        super().__init__("temp")
        self.create()
        super().write(data)

    @staticmethod
    def __generate_a_random_name():
        alp = list(map(chr, range(97, 123)))
        i = 0
        a = []
        while i < 7:
            a.append(Random().choice(alp)) 
            i += 1
        return "".join(a) + "_" + str(randint(100, 100000000))
    
    def create(self):
        """Create the temp file"""
        self.name = self.__generate_a_random_name()
        super().create()
