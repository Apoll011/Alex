from .config import __lang__,path
from .error import Error

#TODO: Change the Translation mechanismes
#Start Translate
__LangExt__ = ".lang"
class GTranslateModule:
    translationIndex = {}
    def __init__ (self, langg = __lang__, file = "system"):
        basePath = path + f"/language/{langg}/tradutor/{file}" + __LangExt__
        f = open(basePath, "r", encoding = "UTF-8").read().splitlines()
        for l in f:
            if l != "":
                tran = l.split(":")
                self.translationIndex[tran[0]] = tran[1].replace("#%", "{}")
    def getTranslation(self, lookup):
        cv = self.translationIndex[lookup]
        return cv

gt = GTranslateModule()

def __(Jumpper, *args):
    """Jumpper = ex: system.tanks
    predef lang = pt
    return Obrigado
    """

    try:
        if(len(args) > 0):
                        return str(gt.getTranslation(Jumpper)).format(*args)
        else:
            return str(gt.getTranslation(Jumpper))
    except KeyError:
                return __("error."+str(Error.get(457)[1]))
    except Exception as e:
        return __("error."+str(Error.get(e)[1]))

class Translator:
    def __init__(self, file= "system", lang = __lang__) -> None:
        self.gt = GTranslateModule(file = file, langg = lang)
    def _(self, Jumpper, *args):
        try:
            if(len(args) > 0):
                            return str(self.gt.getTranslation(Jumpper)).format(*args)
            else:
                return str(self.gt.getTranslation(Jumpper))
        except KeyError:
                    return __("error."+str(Error.get(457)[1]))
        except Exception as e:
            return __("error."+str(Error.get(e)[1]))
