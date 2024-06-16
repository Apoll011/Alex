from nexus.ai import AI
from .functions import priaSkeleton

class PRIA(AI):
    def __init__(self) -> None:
        super().__init__("PRIA")
        self.register_blueprint(priaSkeleton)

