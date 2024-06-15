from core.system.api.call import ApiCall

api = ApiCall("127.0.0.1", 1178)
p = api.call_route("users/search/name", {"query": "Tiago"})
p.then(lambda data: print(data))
        