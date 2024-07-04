from .functions import wecSkeleton
from core.system.ai.ai import AI


class WEC(AI):
    database = {
        
    }
    def __init__(self) -> None:
        super().__init__("WEC")

        self.register_blueprint(wecSkeleton)
