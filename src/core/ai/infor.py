import datetime
import os
from collections import namedtuple
from enum import Enum

import psutil

from core.config import path

class Registries(Enum):
    WAKE_UP = 1
    SYSTEM_ERROR = -1

class Register:
    label: str
    data = []
    backgroundColor: str
    borderColor: str
    borderWidth: int
    
    def __init__(self, label, backgroundColor, borderColor, borderWidth) -> None:
        self.label: str = label
        self.backgroundColor: str = backgroundColor
        self.borderColor: str = borderColor
        self.borderWidth: int = borderWidth

    def __repr__(self) -> str:
        return f'{{"label":  {self.label}, "data": {self.data}, "backgroundColor": {self.backgroundColor}, "borderColor": {self.borderColor}, "borderWidth": {self.borderWidth}}}'
    
class SysInfo:
    sys = {
        "process_given_today": 0,
        "commands_given": 0,
    }
    
    system_data = {
        "cpu": [],
        "net": []
    }
    
    plot = [
                Register("Wake Up", "rgb(255, 9, 13)", "rgba(255,19,12,1)", 1),
            ]
            
    
    
    def system_info(self):
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
        
        try:
            battery = psutil.sensors_battery() or self.get_baterry_default()

        except Exception:
            battery = self.get_baterry_default()
            
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
                "chart": self.system_data,
                "plot": {
                        "datasets": self.plot
                }
            },
            "skills":  [os.listdir(f"{path}/skills/")]
        }
        return system

    def register(self, registe: Registries):
        name = " ".join(registe.name.split("_"))
        name = name.title()
        
        date = datetime.datetime.now()
        
        index = 0
        for registered in self.plot:
            if registered.label == name:
                self.plot[index].data.append({
                    "x": date.hour,
                    "y": date.minute
                })
                return
            index += 1
        
        raise RegisterNotValid(name)

    def get_baterry_default(self):
        sbattery = namedtuple('sbattery', ['percent', 'secsleft', 'power_plugged'])
        battery = sbattery(None, -2, True)
        return battery

class RegisterNotValid(BaseException):
    def __init__(self, name) -> None:
        super().__init__(f"Register {name} Not Valid")