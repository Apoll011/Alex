import time
import requests
from enum import Enum

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

class ApiMethod(Enum):
    GET = 0
    PUT = 1
    POST = 2
    DELETE = 3
    OPTIONS = 4
    PATCH = 5

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
  
    def call_route(self, route: str, value: dict[str, str] = {}, method: ApiMethod = ApiMethod.GET):
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

        url = f"http://{self.HOST}:{self.PORT}/{route}?{t}"

        match method:
            case ApiMethod.GET:
                data = requests.get(url)
            case ApiMethod.PUT:
                data = requests.put(url)
            case ApiMethod.POST:
                data = requests.post(url)
            case ApiMethod.PATCH:
                data = requests.patch(url)
            case ApiMethod.DELETE:
                data = requests.delete(url)
            case ApiMethod.OPTIONS:
                data = requests.options(url)
        
        j = data.json()
        
        if "responce" in j.keys() and len(j.keys()) == 1:
            j = j["responce"]
        d = {"responce": j, "code": data.status_code, "time": time.time() - tie}
        
        return ApiResponse(d)
