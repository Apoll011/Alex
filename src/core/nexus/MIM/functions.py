from .library import Library
from core.system.ai.ai import AI
from core.system.ai.blueprint import AiBluePrintSkeleton

mimSkeleton = AiBluePrintSkeleton()

@mimSkeleton.init_action("Load The Music")
def load_countries(self, mim: AI):
    mim.library.start_import() # type: ignore
    mim.finish(self)
