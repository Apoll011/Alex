from core.system.config import nexus_ai
import os
from core.system.context import ContextManager

class Nexus:
    @staticmethod
    def start():
        cm = ContextManager()
        os.system("clear")
        cm.save(False, "all_ai_started", "pickle")
        for name in nexus_ai:
            path = f"core.nexus.{name}"
            exec("from {} import {}".format(path, name))
            exec(f"{name}().activate()")
        cm.save(True, "all_ai_started", "pickle")
