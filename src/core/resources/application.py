import os

from core.config import USER_RESOURCE_PATH

class Application:
    """Class that work with the application files from Alex"""

    @staticmethod
    def getPath(extension:str):
        """Return the path for the application file."""
        return Application.clear(f"{USER_RESOURCE_PATH}/application/application.{extension}")

    @staticmethod
    def clear(path):
        return path.replace("//", "/")

    @staticmethod
    def load(extension:str):
        """Return the path of the application file. If not found the file create it."""
        if not Application.exist(extension):
            fs = open(Application.getPath(extension), "a")
            fs.close()
            
        return Application.getPath(extension)

    @staticmethod
    def save(extension: str, value: str, opening_type: str = "a"):
        """Save some value into the application file given an extension, value, and type of opening"""
        o = open(Application.load(extension), opening_type)
        o.write(value+"\n")
        o.close()

    @staticmethod
    def get(extension:str):
        if Application.exist(extension):
            with open(Application.getPath(extension), "r") as t:
                return str(t.read()).strip()
        else:
            return ""
    
    @staticmethod
    def exist(extension:str):
        if os.path.isfile(Application.getPath(extension)):
            return True
        else:
            return False
