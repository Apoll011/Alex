import tkinter as tk
from tkinter import messagebox

import pyttsx3
import speech_recognition as sr

from core.interface.base import BaseInterface

class Voice(BaseInterface):
    name = "voice"

    def __init__(self, alex):
        super().__init__(alex)
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.setup_ui()

    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("Alex Voice Interface")

        self.text_area = tk.Text(self.root, height=10, width=50)
        self.text_area.pack(pady=10)

        self.speak_button = tk.Button(self.root, text="Speak", command=self.listen)
        self.speak_button.pack()

    def start(self):
        self.user_connect({})
        super().start()
        self.root.mainloop()

    def listen(self):
        with sr.Microphone() as source:
            self.text_area.insert(tk.END, "\nListening...\n")
            try:
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio)
                self.text_area.insert(tk.END, f"You: {text}\n")
                self.input({"message": text})
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Could not understand audio")
            except sr.RequestError:
                messagebox.showerror("Error", "Could not request results")

    def speak(self, data):
        if data["value"]:
            self.text_area.insert(tk.END, f"Alex: {data['value']}\n")
            self.engine.say(data["value"])
            self.engine.runAndWait()

    def loop(self):
        self.root.update_idletasks()
        self.root.update()
        super().loop()
