import socket

import requests

from core.config import API_SEARCH_TIMEOUT

def is_device(ip):
    try:
        responce = requests.get(f"http://{ip}/", timeout=API_SEARCH_TIMEOUT)
        if responce.json()["name"] != "Alex-Bot":
            raise KeyError
        return True
    except (KeyError, Exception):
        return False

def get_device_on_local_net():
    local_ip = socket.gethostbyname(socket.gethostname())

    ip_parts = local_ip.split(".")
    base_ip = ".".join(ip_parts[:-1])

    for i in range(1, 255):
        ip = f"{base_ip}.{i}"
        url = f"http://{ip}/"

        try:
            if is_device(ip):
                return ip
        except (requests.ConnectionError, requests.Timeout):
            pass
    return None
