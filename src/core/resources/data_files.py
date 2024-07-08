import os
from core.system.config import path

class DataFile:
    @staticmethod
    def getPath(name:str, extension:str):
        """Return the path for the data file."""
        return f"{path}/resources/data/{extension}/{name}.{extension}"

    @staticmethod
    def load(name, extension, create_if_not = True):
        if not DataFile.exist(name, extension): 
            if create_if_not:
                fs = open(DataFile.getPath(name,extension), "a")
                fs.close()
        return DataFile.getPath(name,extension)
    
    @staticmethod
    def save(name, extension, value, type = "a"):
        if DataFile.exist(name, extension):
            o = open(DataFile.getPath(name,extension), type)
            o.write(value)
            o.close()
    
    @staticmethod
    def get(name, extension):
        if DataFile.exist(name, extension):
            with open(DataFile.getPath(name,extension), "r") as t:
                return str(t.read())
        else:
            return ""
    
    @staticmethod
    def exist(name, extension):
        if os.path.isfile(DataFile.getPath(name,extension)):
            return True
        else:
            return False

class List(DataFile):
    extension = "list"

    @staticmethod
    def load(name, create_if_not=True):
        return DataFile.load(name, List.extension, create_if_not)

    @staticmethod
    def get(name):
        l = DataFile.get(name, List.extension).splitlines()
        list = {}
        for li in l:
            list[li.split("::")[0]] = li.split("::")[1]
        return list
