import os
import json
import socket
import threading

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

class RecurrentApiClient:
    def __init__(self, host, port, callback_on_responce = lambda data: print(data.response)):
        self.HOST = host
        self.PORT = port
        self.callback_on_responce = callback_on_responce

        self.connect()
        threading.Thread(target=self.loop).start()

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        self.conection = s

    def loop(self):
        while True:
            data = self.conection.recv(1024).decode("utf-8")
            if data == None or data == "":
                continue
            d = data.split("}{")
            for dat in d:
                if not dat.endswith("}"):
                    dat += "}"
                self.callback_on_responce(ApiResponse(json.loads(dat)))

    def close_server(self):
        """
        Close the server
        """
        self.__send("close")
        self.active = False
        self.close()

    def call_route(self, route: str, value: str | dict[str, str] = ""):
        """
        Calls a route synchronously.

        Args:
            route (str): The route to call.
            value (str | dict[str, str]): The value to pass to the route (default: "").

        Returns:
            An ApiResponse object.
        """
        self.__send(route, value)

    def __send(self, route: str, value: str | dict[str, str] = ""):
        d = {"route": route, "value": value}
        self.conection.send(bytes(json.dumps(d).encode("utf-8")))
    
    def close(self):
        self.conection.close()

def responce(data: ApiResponse):
    d = data.response
    match d:
        case {"responce": True}:
            pass

        case {"value": ""}:
            pass

        case {"type": "say"}:
            print(f"\n\33[0m{d["settings"]["voice"]}: \33[36m{d['value']}\33[0m")
            print("Your request: ")

        case {"type": "play_audio"}:
            os.system(f"afplay {d["value"]}")

        case _:
            print(d)


try:
    client = RecurrentApiClient("127.0.0.1", 1287, responce)

    while True:
        m = input("Your request: ")
        client.call_route("alex/input", json.dumps({"message": m}))

except KeyboardInterrupt:
    client.close()
