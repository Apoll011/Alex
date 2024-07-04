from .library import Library
from .functions import mimSkeleton
from core.system.ai.ai import AI

class MIM(AI):
    def __init__(self) -> None:
        super().__init__("MIM")
        self.library = Library()
        self.register_blueprint(mimSkeleton)
