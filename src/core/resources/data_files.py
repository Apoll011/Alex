import os
from core.config import path

class DataFile:
    @staticmethod
    def getPath(name:str, extension:str):
        """Return the path for the data file."""
        return f"{DataFile.getBasePath(extension)}{name.replace(" ", "_")}.{extension}"

    @staticmethod
    def getBasePath(extension:str):
        """Return the path for the data file."""
        return f"{path}/resources/data/{extension}/"

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
        else:
            DataFile.load(name, extension)
            DataFile.save(name, extension, value, type)
    
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

    @staticmethod
    def delete(name, extension):
        os.remove(DataFile.load(name, extension))

class Dict(DataFile):
    extension = "dict"

    @staticmethod
    def load(name, create_if_not=True):
        return DataFile.load(name, Dict.extension, create_if_not)

    @staticmethod
    def get(name):
        l = DataFile.get(name, Dict.extension).splitlines()
        list = {}
        for li in l:
            list[li.split("::")[0]] = li.split("::")[1]
        return list

class List(DataFile):
    extension = "list"

    @staticmethod
    def load(name, create_if_not=True):
        return DataFile.load(name, List.extension, create_if_not)

    @staticmethod
    def get(name):
        l = DataFile.get(name, List.extension).splitlines()
        if "" in l:
            l.remove("")
        return l

    @staticmethod
    def append(name, value):
        if len(List.get(name)) == 0:
            List.save(name, value, "a")
        else:
            List.save(name, "\n"+value, "a")

    @staticmethod
    def save(name, value, type = "a"):
        if isinstance(value, list):
            DataFile.save(name, List.extension, "\n".join(value), type)
        else:
            DataFile.save(name, List.extension, value, type)
    
    @staticmethod
    def exist(name):
        return DataFile.exist(name, List.extension)

    @staticmethod
    def delete(name, extension):
        DataFile.delete(name, List.extension)

    @staticmethod
    def getPath(name):
        return DataFile.getPath(name, List.extension)
    
    @staticmethod
    def getBasePath():
        return DataFile.getBasePath(List.extension)

    @staticmethod
    def element_exists(name, element) -> bool:
        list_content = List.get(name)
        if element in list_content:
            return True
        else:
            return False
