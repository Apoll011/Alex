import time
import psutil
import threading
from core.log import LOG
from core.ai.ai import AI
from core.config import *
from collections import namedtuple

class BaseInterface:
    closed = False
    _registry: 'BaseInterface'
    _name: str

    request_sentence: str

    waiting_for_message = False
    
    sys = {
        "process_given_today": 0,
        "comands_given": 0,
    }

    def __init__(self, alex: AI):
        self.alex = alex
        self.register()
    
    def init(self):
        LOG.info(f"Started interface {self.__class__.__name__}")
        self.print_header()
        self.request_sentence = self.alex.translate("system.request")
        self.alex.interface_on() 
        self.alex.start()


    def print_header(self):
        print("Starting on interface:\33[32m", self.__class__.__name__,"\33[0m")
    
    def start(self):
        loop = threading.Thread(name = "MainLoop", target=self.start_loop)
        loop.start()
        while not self.closed:
            self.loop()

    def start_loop(self): 
        while not self.closed:
            time.sleep(ALEX_LOOP_DELAY)
            self.alex.loop()

    def speak(self, data): ...
    
    def input(self, data): 
        message = data['message']
        message_processed = self.process_input(message)
        self.alex.process(message_processed)
        self.sys["comands_given"] += 1
        
    def wakeword(self, data):
        self.alex.wake(data)
        self.on_wake_word()

    def on_wake_word(self): ...
    
    def parse(self, data): ...
    
    def execute(self, comand): ...

    def loop(self): 
        self.sys["process_given_today"] += 1

    def close(self):
        LOG.info("Deactivating Alex")
        self.closed = True
        LOG.info("Closed Alex")

    def user_conect(self, data):
        LOG.info("User Conected")
        self.alex.handle_request("userConect")
        
    def change_mode(self, data: dict):
        self.alex.handle_request("changeMode", data["mode"])

    def register(self) -> None:
        """
        Registers the Interface
        """
        BaseInterface._registry = self
        BaseInterface._name = self.__class__.__name__

    @classmethod
    def get(cls):
        return cls._registry
    
    @classmethod
    def is_set(cls):
        if cls._registry:
            return True
        return False

    @classmethod
    def get_name(cls):
        return cls._name
    
    def process_input(self, text: str):
        text = text.strip()
        text = text.replace("×", " times ").replace("÷", " over ").replace("+", " plus ").replace("-", " minus ")
        return text

    def process(self, data):
        type = data["type"]

        match type:
            case "say":
                self.speak(data)

            case "play_audio":
                os.system(f"afplay {data['value']}")

            case _:
                raise KeyError(f"The type {type} is not valid")

    def system_info(self):
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
        
        try:
            battery = psutil.sensors_battery()
        except Exception:
            sbattery = namedtuple('sbattery', ['percent', 'secsleft', 'power_plugged'])
            battery = sbattery(None, -2, True)

        disk = psutil.disk_usage(".")
        info = {
            "cpu": cpu,
            "memory": memory,
            "battery": {
                "total": battery.percent,
                "seconds_left": battery.secsleft,
                "plugged": battery.power_plugged
            },
            "disk": {
                "total": disk.total, 
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent
            }
        }
        
        system = {
            "status": ["ok", "warning", "error", "suspended", "hiberning"],
            "info": info,
            "data": {
                "process_exec_t": self.sys["process_given_today"],
                "comands_gt": self.sys["comands_given"],
                "errors_t":"0",
                "chart": self.alex.system_data,
                "plot": {
                        "datasets": [
                        {
                            "label": "Wake Up",
                            "data": [{
                                "x": 10,
                                "y": 0
                            },
                            {
                                "x": 2,
                                "y": 3
                            }],
                            "backgroundColor": "rgb(255, 9, 13)",
                            "borderColor": "rgba(255,19,12,1)",
                            "borderWidth": 1
                        },
                        {
                            "label": "Api Calls",
                            "data": [{
                                "x": 11,
                                "y": 53
                            },
                            {
                                "x": 12,
                                "y": 30
                            },
                            {
                                "x": 10,
                                "y": 5
                            }
                            ],
                            "backgroundColor": "rgb(54, 162, 235)",
                            "borderColor": "rgba(54, 192, 235, 1)",
                            "borderWidth": 1
                        }
                        ]
                }
            },
            "skills":  [{"name": str,"id": str,"cpu": int, "internetDialy": int, "status": ["running", "warning", "error"]}]
        }
        return info
