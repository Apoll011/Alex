

class Api:
    responce: dict
    code: int
    time: float

    def __init__(self, data: dict) -> None:
        self.responce = data["responce"]
        self.code = data["code"]
        self.time = data["time"]
