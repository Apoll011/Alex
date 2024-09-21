import datetime

from core.interface.base import BaseInterface
from core.security.code import AlexKey

class API(BaseInterface):
    name = "api"
    def start(self):
        # self.register_fun("alex/wake", self.wakeword)
        # self.register_fun("alex/change/mode", self.change_mode)
        # self.register_fun("alex/user/conect", self.user_connect)
        # self.register_fun("alex/api/call", self.api_call)
        # self.register_fun("alex/info", self.info)
        # self.register_fun("alex/info/user", self.user)
        # self.server.set_route("alex/input", self.input)
        super().start()
    

    def register_fun(self, route, callback) -> None:
        # self.server.set_route(route, lambda data: self.run_return(callback, {} if data == None or data == "" else json.loads(data)))
        pass

    @staticmethod
    def run_return(fun, data):
        f = fun(data)
        if f is None:
            return {"responce": True}
        else:
            return f

    def api_call(self, data):
        return self.alex.api.call_route(data["route"], data["value"]).response

    @staticmethod
    def info(data):
        return {
                "type": "info",
                "device_id": AlexKey.get(),
                "update_date": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            }

    def user(self, data):
        return self.alex.get_context("master")
"""
S
    /alex/info/system/, {}, {
            "data": {
                "process_exec_t": "1042",
                "comands_gt": "62",
                "net_com": "6236",
                "data_fls": "5235",
                "errors_t":"2",
                "chart": {
                    "cpu_usage": [19, 48, 70, 60, 63, 56, 33, 17, 59, 21, 36, 12, 39, 59, 62, 23, 12, 8, 9, 4, 6, 10, 2, 5, 19],
                    "internet_usage": [3, 16, 39, 50, 35, 48, 24, 0, 29, 1, 5, 0, 24, 34, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 3]
                },
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
            }
        }
    /alex/info/hardware/, {}, {"cpu": str,"disk_usage": str,"ram": str,"batery": str,"internet": str,"status": ["ok", "warning", "error", "suspended", "hiberning"]}
    /alex/notifications, {}, [{"title": str,"date": str,"description": str,"icon": ["info-alt", "user", "settings"],"bg": ["success", "info", "error", "warning"],"costume_class": ["infinite-spin", None]},...]
    /alex/notifications/important, {}, [{"title": str,"options": {"body": str,"icon": "",}},...]
    /alex/skills, {}, [{"name": str,"id": str,"cpu": int, "internetDialy": int, "status": ["running", "warning", "error"]}]

"""
