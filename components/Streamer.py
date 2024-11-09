import socket
import json

class Streamer:
    def __init__(self, PORT=5005):
        self.sendObj = {}
        self.host = "127.0.0.1"
        self.port = PORT
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Change to TCP

        # # Connect to the receiver (server)
        # self.sock.connect((self.host, self.port))

    def stream(self):
        # Convert the object to JSON string
        message = json.dumps(self.sendObj)

        # Send the message over TCP
        self.sock.sendall(message.encode())  # Send the entire message in one go

        # Clear the send object after sending
        self.sendObj = {}

    def stop(self):
        self.sock.close()
