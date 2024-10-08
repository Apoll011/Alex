import socket

import requests

from core.config import API_SEARCH_TIMEOUT, config_file

def is_base_server(ip):
    try:
        responce = requests.get(f"http://{ip}:{config_file["api"]["port"]}/")
        if responce.json()["name"] != "Alex":
            raise KeyError
        return True
    except (KeyError, Exception):
        return False

def get_base_server_on_local_net():
    local_ip = socket.gethostbyname(socket.gethostname())

    ip_parts = local_ip.split(".")
    base_ip = ".".join(ip_parts[:-1])

    for i in range(1, 255):
        ip = f"{base_ip}.{i}"
        url = f"http://{ip}:{config_file["api"]["port"]}/"

        try:
            responce = requests.get(url, timeout=API_SEARCH_TIMEOUT)
            if responce.status_code == 200:
                data = responce.json()
                if "name" in data and data["name"] == "Alex":
                    return ip
        except (requests.ConnectionError, requests.Timeout):
            pass
    return None
