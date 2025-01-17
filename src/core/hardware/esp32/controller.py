import struct
import threading
import time
import wave
from queue import Queue

import bluetooth

from core.hardware.esp32.animation_controller import AnimationController
from core.hardware.esp32.button_handler import ButtonHandler
from core.resources.application import Application

class ESP32BluetoothClient:
    def __init__(self):
        self.socket = None
        self.connected = False
        self.audio_queue = Queue()
        self.device_name = "Alex-Box"
        self.animation_controller = AnimationController(self.send_message)
        self.button_handler = ButtonHandler()

    def scan_and_connect(self):
        """Scan for and connect to ESP32 device"""
        target_address = None
        saved = Application.get("box_mac")
        if saved != "":
            target_address = saved
            try:
                return self.connect(target_address)
            except:
                pass

        devices = bluetooth.discover_devices(lookup_names=True)
        for addr, name in devices:
            if name == self.device_name:
                target_address = addr
                break

        return self.connect(target_address)

    def connect(self, target_address):
        if target_address:
            self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.socket.connect((target_address, 1))
            self.connected = True

            # Start receiver thread
            threading.Thread(target=self._receive_messages, daemon=True).start()
            self.send_message("CONNECT")
            Application.save("box_mac", target_address, "w")
            return True
        else:
            return False

    def send_message(self, message):
        """Send text message to ESP32"""
        if self.connected:
            self.socket.send(message.encode() + b"\n")

    def stream_audio(self, wav_file):
        """Stream audio from WAV file to ESP32"""
        if not self.connected:
            print("Not connected to ESP32")
            return

        try:
            with wave.open(wav_file, "rb") as wav:
                chunk_size = 256  # Adjust based on your needs

                while True:
                    data = wav.readframes(chunk_size)
                    if not data:
                        break

                    # Format audio packet with header and length
                    length = len(data)
                    header = b"AUD:" + struct.pack(">H", length)
                    self.socket.send(header + data)
                    time.sleep(0.02)  # Adjust timing based on your needs

        except Exception as e:
            print(f"Error streaming audio: {e}")

    def _receive_messages(self):
        """Background thread to receive messages"""
        while self.connected:
            try:
                data = self.socket.recv(1024)
                if data:
                    self.button_handler.on_button_pressed(data)
            except:
                break

    def close(self):
        """Close the connection"""
        if self.socket:
            self.send_message("DISCONNECT")
            self.connected = False
            self.socket.close()
