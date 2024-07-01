import time
from core.system.ai.ai import AI
from .functions import alexSkeleton


class ALEX(AI):

    mode: str

    def __init__(self) -> None:
        super().__init__("ALEX")
        self.register_blueprint(alexSkeleton)
        self.internet_is_on = False
        self.server_mode = False
                

    def start(self):
        self.clear()
        print("Hi", self.get_context("master")["name"])  # type: ignore
        super().start()

    def loop(self):
        int = self.listen()
        text_returned, intent = self.process(int)
        if text_returned != None:
            self.speak(str(text_returned))
    
    def listen(self, data = None):
        if data == None:
            if self.internet_is_on:
                time.sleep(1)
                r = super().listen().strip()
            else:
                r = input("Seu texto: ")

            if r == "":
                return self.listen()
            
            if self.debug_mode:
                print("Input: ", r)
            
            return r
        else:
            return data['message']
    
    def handle_send_message(self, data):
        message = self.listen(data)
        m, intent = self.process(message)
        if m != None:
            pass
            #emit('receive_message', {'message': m}, broadcast=True)

    def speak(self, text: str, voice: str = 'Alex', voice_command=None):
        if self.debug_mode:
            print("Alex: ", text)
        return super().speak(text, voice, voice_command)

    def change_mode(self, data: dict):
        self.handle_request("changeMode", data["mode"])
