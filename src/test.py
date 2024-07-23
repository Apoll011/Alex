from core.api.client import ApiClient

client = ApiClient("127.0.0.1", 1287)

while True:
    route = input("The route: ")
    value = input("The value: ")
    r = client.call_route(route, value)
    print(r.response)
