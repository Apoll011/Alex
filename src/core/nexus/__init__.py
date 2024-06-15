from ..system.config import nexus_ai
import os

class Nexus:
    @staticmethod
    def start():
        os.system("clear")
        for name in nexus_ai:
            path = f"core.nexus.{name}"
            exec("from {} import {}".format(path, name))
            exec(f"{name}().activate()")
