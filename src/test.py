# client.py (Standalone program)
import json
import socket
import sys
import threading
from abc import ABC, abstractmethod

class AlexAPIClient(ABC):
    client_socket: socket.socket

    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.closed = False
        self.receive_thread = None

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            self.connected = True

            # Start receive thread
            self.receive_thread = threading.Thread(target=self._receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            self.on_connection(True)
            return True
        except Exception as e:
            self.on_connection(False)
            return False

    def _receive_messages(self):
        while not self.closed and self.connected:
            try:
                data = self.client_socket.recv(4096 * 2)
                if data:  # We received something
                    message = json.loads(data.decode())
                    self.output(message)
            except (ConnectionError, Exception):
                continue
            except json.JSONDecodeError:
                self.on_error_receiving_msg("Invalid JSON received")
            except Exception as e:
                if not self.closed:
                    self.on_error_receiving_msg(f"Error receiving message: {e}")
                break

        self.connected = False
        self.on_disconnect()
        sys.exit(1)

    def input(self, text):
        if self.connected:
            try:
                message = {"type": "input", "message": text}
                self.client_socket.send(json.dumps(message).encode())
            except Exception as e:
                self.on_error_sending_msg(f"Error sending message: {e}")

    def close(self):
        self.closed = True
        if self.connected:
            self.client_socket.close()
            self.on_close()

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def on_disconnect(self):
        pass

    @abstractmethod
    def output(self, data):
        pass

    @abstractmethod
    def on_connection(self, successful):
        pass

    @abstractmethod
    def on_error_receiving_msg(self, error):
        pass

    @abstractmethod
    def on_error_sending_msg(self, error: str) -> None:
        pass

    @abstractmethod
    def on_close(self):
        pass

class CmdClient(AlexAPIClient):

    def on_disconnect(self):
        print("\nDisconnected from server")

    def output(self, data):
        message_type = data.get("type")
        if message_type == "message" and data['content'] != "":
            print(f"{data['voice']}: {data['content']}")
            print("Your input: ", end="", flush=True)

    def on_connection(self, successful):
        if successful:
            print("Connected successfully!")
        else:
            print(f"Failed to connect to server.")

    def on_error_receiving_msg(self, error):
        print(error)

    def on_error_sending_msg(self, error: str) -> None:
        print(error)

    def on_close(self):
        print("Closed the connection.")

    def run(self):
        if not self.connect():
            return

        try:
            while self.connected:
                try:
                    user_input = input()
                    if user_input.lower() in ["quit", "exit"]:
                        break
                    self.input(user_input)
                except EOFError:
                    break
        except KeyboardInterrupt:
            print("\nClosing connection...")
        finally:
            self.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Network Client for Alex")
    parser.add_argument("--host", default="localhost", help="Server host address")
    parser.add_argument("--port", type=int, default=5927, help="Server port")

    args = parser.parse_args()

    client = CmdClient(host=args.host, port=args.port)
    client.run()
