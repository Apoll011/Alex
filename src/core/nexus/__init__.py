from ..system.config import nexus_ai

class Nexus:
    @staticmethod
    def start():
        for name in nexus_ai:
            path = f"core.nexus.{name}"
            exec("from {} import {}".format(path, name))
            exec(f"{name}().activate()")
