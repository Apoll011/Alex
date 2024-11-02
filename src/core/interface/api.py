# server.py
import json
import socket
import threading
from typing import Dict

from core.interface.base import BaseInterface

class API(BaseInterface):
    name = "server"

    def __init__(self, alex, host="localhost", port=5000):
        super().__init__(alex)
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients: Dict[socket.socket, str] = {}
        self.clients_lock = threading.Lock()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        # Start client acceptance thread
        accept_thread = threading.Thread(target=self._accept_clients)
        accept_thread.daemon = True
        accept_thread.start()

        super().start()

    def _accept_clients(self):
        while not self.closed:
            try:
                client_socket, address = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self._handle_client, args=(client_socket,)
                )
                client_thread.daemon = True
                client_thread.start()
            except Exception as e:
                if not self.closed:
                    print(f"Error accepting client: {e}")

    @staticmethod
    def _receive_with_timeout(socket: socket.socket, timeout=1.0):
        """Helper function to receive data with timeout"""
        try:
            data = socket.recv(4096)
            return data
        except ConnectionError:
            return False

    def _handle_client(self, client_socket: socket.socket):
        try:
            # Register client
            with self.clients_lock:
                self.clients[client_socket] = str(client_socket.getpeername())

            self.user_connect({"client": str(client_socket.getpeername())})

            while not self.closed:
                try:
                    data: None | bool | bytes = self._receive_with_timeout(client_socket)
                    if data is False:  # Connection error
                        continue
                    if data:  # We received something
                        message = json.loads(data.decode())
                        self.input(message)
                except json.JSONDecodeError:
                    print("Invalid JSON received")
                except Exception as e:
                    print(f"Error handling client message: {e}")
                    break

        finally:
            with self.clients_lock:
                if client_socket in self.clients:
                    del self.clients[client_socket]
            client_socket.close()

    def speak(self, data):
        # Convert internal message format to client format
        client_message = {
            "type": "message",
            "voice": data["settings"]["voice"],
            "content": data["value"],
        }

        # Broadcast message to all clients
        message = json.dumps(client_message).encode()
        with self.clients_lock:
            disconnected_clients = []
            for client_socket in self.clients:
                try:
                    client_socket.send(message)
                except:
                    disconnected_clients.append(client_socket)

            # Clean up disconnected clients
            for client_socket in disconnected_clients:
                del self.clients[client_socket]
                client_socket.close()

    def close(self):
        self.closed = True
        with self.clients_lock:
            for client_socket in self.clients:
                client_socket.close()
            self.clients.clear()
        self.server_socket.close()
        super().close()
