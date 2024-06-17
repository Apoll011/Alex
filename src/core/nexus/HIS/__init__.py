from core.nexus.ai import AI

class HIS(AI):
    h = False
    f = False
    def __init__(self) -> None:
        super().__init__("HIS")
        self.h = True
    
    def activate(self):
        self.f = True
        super().activate()
