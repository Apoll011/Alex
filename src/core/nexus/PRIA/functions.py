from core.system.ai.ai import AI
from core.system.config import api
from core.system.api.client import ApiClient
from core.system.security._key import AlexKey
from core.system.ai.blueprint import AiBluePrintSkeleton

priaSkeleton = AiBluePrintSkeleton()

@priaSkeleton.init_action("Set Api conection")
def set_api_con(self, pria: AI):
    pria.api = ApiClient(api['host'], api['port'])
    pria.finish(self)

@priaSkeleton.init_action("Get Master User")
def get_master_user(self, pria: AI):
    p = pria.api.call_route_async("users/search/tags", {"query": "Master"})
    p.then(lambda user: pria.finish_and_set(self, "master", pria.api.call_route("users/get", user.response["users"][0]).response))

@priaSkeleton.init_action("Set context")
def set_context(self, pria: AI):
    pria.set_context("key", AlexKey.get())
    pria.finish(self)
