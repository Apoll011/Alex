from ..ai import AiInitActionBlueprint
from ...system.api.call import ApiCall

priaInitAction = AiInitActionBlueprint()
api = ApiCall("127.0.0.1", 1178)


@priaInitAction.init_action("Get Master User")
def get_master_user(pria):
    p = api.call_route_async("users/search/tags", {"query": "Master"})
    p.then(lambda user: pria.finish_and_set("Get Master User", "master", user.responce["users"][0]))
