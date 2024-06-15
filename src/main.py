from core.system.api.call import ApiCall

api = ApiCall("127.0.0.1", 1178)
p = api.call_route_async("users/search/name", {"query": "Bernardo"})
p.then(lambda data: print(data.responce["users"]))
print("Hi")
print(p.value.time)
