# client.py (Standalone program)
import json
import socket
import sys
import threading

class StandaloneClient:
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.closed = False
        self.receive_thread = None

    def connect(self):
        try:
            print(f"Connecting to server at {self.host}:{self.port}...")
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            print("Connected successfully!")

            # Start receive thread
            self.receive_thread = threading.Thread(target=self._receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()

            return True
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return False

    def _receive_messages(self):
        while not self.closed and self.connected:
            try:
                data: bool | None | bytes = self._receive_with_timeout(self.client_socket)
                if data is False:  # Connection error
                    continue
                if data:  # We received something
                    message = json.loads(data.decode())
                    self._handle_message(message)
            except json.JSONDecodeError:
                print("Invalid JSON received")
            except Exception as e:
                if not self.closed:
                    print(f"Error receiving message: {e}")
                break

        self.connected = False
        print("\nDisconnected from server")
        sys.exit(1)

    def _handle_message(self, message):
        message_type = message.get("type")
        if message_type == "message" and message['content'] != "":
            print(f"\n{message['voice']}: {message['content']}")
            print("Your input: ", end="", flush=True)
        elif message_type == "system":
            print(f"\nSystem: {message['message']}")
            print("Your input: ", end="", flush=True)

    def send_input(self, text):
        if self.connected:
            try:
                message = {"type": "input", "message": text}
                self.client_socket.send(json.dumps(message).encode())
            except Exception as e:
                print(f"Error sending message: {e}")
                self.connected = False

    def run(self):
        if not self.connect():
            return

        try:
            while self.connected:
                try:
                    user_input = input()
                    if user_input.lower() in ["quit", "exit"]:
                        break
                    self.send_input(user_input)
                except EOFError:
                    break
        except KeyboardInterrupt:
            print("\nClosing connection...")
        finally:
            self.close()

    def close(self):
        self.closed = True
        if self.connected:
            self.client_socket.close()

    @staticmethod
    def _receive_with_timeout(socket, timeout=1.0):
        """Helper function to receive data with timeout"""
        try:
            data = socket.recv(4096)
            return data
        except (ConnectionError, Exception):
            return False

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Network Client for Alex")
    parser.add_argument("--host", default="localhost", help="Server host address")
    parser.add_argument("--port", type=int, default=5000, help="Server port")

    args = parser.parse_args()

    client = StandaloneClient(host=args.host, port=args.port)
    client.run()
