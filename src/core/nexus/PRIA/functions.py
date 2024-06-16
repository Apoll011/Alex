from ..ai import AiBluePrintSkeleton, AI
from ...system.api.call import ApiCall
from core.system.security._key import AlexKey

priaSkeleton = AiBluePrintSkeleton()
api = ApiCall("127.0.0.1", 1178)

@priaSkeleton.init_action("Get Master User")
def get_master_user(self, pria):
    p = api.call_route_async("users/search/tags", {"query": "Master"})
    p.then(lambda user: pria.finish_and_set(self, "master", user.responce["users"][0]))

@priaSkeleton.init_action("Set context")
def set_context(self, pria: AI):
    pria.set_context("key", AlexKey.get())
    pria.finish(self)
