from core.nexus.ai import AiBluePrintSkeleton, AI
from core.system.api.call import ApiCall

alexSkeleton = AiBluePrintSkeleton()

@alexSkeleton.init_action("Set Api conection")
def set_api_con(self, alex: AI):
    alex.api = ApiCall("127.0.0.1", 1178)
    alex.finish(self)

@alexSkeleton.init_action("Train intents")
def train_intents(self, alex: AI):
    promise = alex.api.call_route_async("intent_recognition/train", "pt-pt")
    promise.then(lambda data: alex.finish(self))
