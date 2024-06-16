from core.nexus.ai import AI

class ALEX(AI):
    def __init__(self) -> None:
        super().__init__("ALEX")

    def start_on(self):
        print("Hi", self.get_context("master")["name"])
