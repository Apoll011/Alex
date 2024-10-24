import datetime
import os
from collections import namedtuple
from enum import Enum

import psutil

from core.config import SOURCE_DIR
from core.error import RegisterNotValid

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
    process_given_today = 0,
    commands_given = 0

    system_data = {
        "cpu": [],
        "net": []
    }
    
    plot = [
                Register("Wake Up", "rgb(255, 9, 13)", "rgba(255,19,12,1)", 1),
            ]
            
    
    
    def system_info(self):
        """
        Return the system info
        :return: dict contain info about the system,
        """
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
        
        try:
            battery = psutil.sensors_battery() or self.get_battery_default()

        except (Exception, ValueError):
            battery = self.get_battery_default()
            
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
            "status": ["ok", "warning", "error", "suspended", "hibernating"],
            "info": info,
            "data": {
                "process_exec_t": self.process_given_today,
                "commands_gt": self.commands_given,
                "errors_t":"0",
                "chart": self.system_data,
                "plot": {
                        "datasets": self.plot
                }
            },
            "skills": [os.listdir(f"{SOURCE_DIR}/skills/")]
        }
        return system

    def register(self, register: Registries) -> None:
        """
        Register an action in the system
        :param register: Its the action to register in the system. Type (Registries)
        """
        name = " ".join(register.name.split("_"))
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

    @staticmethod
    def get_battery_default():
        """
        GEt the battery info default values
        :return: The battery info in a tuple representing ('percent', 'secsleft', 'power_plugged')
        """
        sbattery = namedtuple('sbattery', ['percent', 'secsleft', 'power_plugged'])
        battery = sbattery(None, -2, True)
        return battery