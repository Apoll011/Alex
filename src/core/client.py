import time
from enum import Enum

import requests

from core.error import ServerClosed

class ApiResponse:
    response: dict
    """
    This is the response returned by the server
    """
    code: int
    """
    The code returned by the server:
        `200`: `Ok`
        `400`: `Route Not Found`
        `500`: `Server error`. (Description on response)
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

def make_request(url: str, method: ApiMethod):
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

    return data.json(), data.status_code

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

        try:
            self.authenticate()
        except Exception:
            raise ServerClosed()
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

    def call_route(self, route: str, value=None, method: ApiMethod = ApiMethod.GET):
        """
        Calls a route synchronously.

        Args:
            :param route: The route to call.
            :param value: The value to pass to the route (default: "").
            :param method:

        Returns:
            An ApiResponse object.
        """

        if value is None:
            value = {}
        url = self.generate_url(route, value)

        started_time = time.time()

        json_responce, status_code = make_request(url, method)

        return self.create_responce_obj(json_responce, status_code, started_time)

    def generate_url(self, route: str, value):
        key_value = ""
        for key in value.keys():
            key_value += f"{key}={value[key]}"

        url = f"http://{self.HOST}:{self.PORT}/{route}?{key_value}"

        return url

    @staticmethod
    def create_responce_obj(json_data, status_code, started_time):
        if "responce" in json_data.keys() and len(json_data.keys()) == 1:
            json_data = json_data["responce"]

        data = {
            "responce": json_data,
            "code": status_code,
            "time": time.time() - started_time,
        }

        return ApiResponse(data)
