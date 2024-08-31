import time
import requests

class ApiResponse:
    response: dict
    """
    This is the responce returned by the server
    """
    code: int
    """
    The code returned by the server:
        `200`: `Ok`
        `400`: `Route Not Found`
        `500`: `Server error`. (Description on responce)
    """
    time: float
    """
    Time in `seconds` that it took to return an answer
    """

    def __init__(self, data: dict) -> None:
        """
        Initializes the API response.

        Args:
            data (dict): The response data.
        """
        self.response = data["responce"]
        self.code = data["code"]
        self.time = data["time"]

class ApiClient:
    HOST: str
    PORT: int

    active = False

    def __init__(self, host, port):
        """
        Initializes the API client.

        Args:
            host (str): The host address.
            port (int): The port number.
        """
        self.HOST = host
        self.PORT = port

        self.authenticate()

    def authenticate(self):
        """
        Authenticates the client.
        """
        data = self.call_route("alex/alive")
        self.__auth(data)
    
    def __auth(self, data: ApiResponse):
        """
        Authenticates the client.

        Args:
            data (ApiResponse): The authentication response.
        """
        if data.response["on"]:
            self.active = True
    
    def close_server(self):
        """
        Close the server
        """
        self.active = False
  
    def call_route(self, route: str, value: dict[str, str] = {}):
        """
        Calls a route synchronously.

        Args:
            route (str): The route to call.
            value (str | dict[str, str]): The value to pass to the route (default: "").

        Returns:
            An ApiResponse object.
        """
        t = ""
        for key in value.keys():
            t += f"{key}={value[key]}" 
        tie = time.time()
        data = requests.get(f"http://{self.HOST}:{self.PORT}/{route}?{t}")
        j = data.json()
        if "responce" in j.keys() and len(j.keys()) == 1:
            j = j["responce"]
        d = {"responce": j, "code": data.status_code, "time": time.time() - tie}
        return ApiResponse(d)
