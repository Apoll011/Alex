import json
import socket
from ..promise import Promise
from .api import Api

class ApiCall:
    HOST:str
    PORT:int 

    active = False
    
    def __init__(self, host, port):
        """
        Init the Alex Api Call, send the `host` and `port` for the `AlexBaseApi` 
        """
        self.HOST = host
        self.PORT = port

        self.autenticate()

    def autenticate(self):
        promisse = self.call_route_async("alex/alive")
        promisse.then(lambda data: self.__auth(data))

    def __auth(self, data):
        if data["on"] == True:
            self.active = True

    def call_route_async(self, route, value: str | dict[str, str] = ""):
        """
        Will call a route in the `AlexBaseApi` and return a `Promise` for when the result gets back
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        d = {"route": route, "value": value}
        s.send(bytes(json.dumps(d).encode("utf-8")))
        promise = Promise()
        promise.resolve(lambda: self.__get_info(s, promise))
        return promise
    
    def call_route(self, route, value: str | dict[str, str] = ""):
        """
        Will call a route in the `AlexBaseApi` and return the recived `JSON`
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        d = {"route": route, "value": value}
        s.send(bytes(json.dumps(d).encode("utf-8")))
        data = s.recv(1024).decode("utf-8")
        return Api(json.loads(data))


    def __get_info(self, s, promise):
        try:
            data = s.recv(1024).decode("utf-8")
            promise.resolve(lambda: Api(json.loads(data)))
            s.close()  # Close the socket object
        except socket.error as e:
            promise.reject(e)
            s.close()  # Close the socket object
        except json.JSONDecodeError as e:
            promise.reject(e)
            s.close()  # Close the socket object

