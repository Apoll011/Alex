from core.system.api.call import ApiCall
from datetime import datetime

api = ApiCall("127.0.0.1", 1178)
p = api.call_route("intent_recognition/train", "pt-pt")
print(p.responce)
while True:
    int = input("Seu texto: ")
    promesa = api.call_route("intent_recognition/recognize", {"lang": "pt-pt", "text": int})
    r = promesa.responce
    print("A resposta para a entrada", int, "foi", r)
    if r['intent_name'] == "system@time":
        print(datetime.now())
