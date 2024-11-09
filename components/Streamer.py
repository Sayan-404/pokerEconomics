import socket
import json

class Streamer:
    def __init__(self):
        self.sendObj = {}
        self.host = "127.0.0.1"
        self.port = 5005
        
        # UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def stream(self):
        message = json.dumps(self.sendObj)
        self.sendObj = {}
        self.sock.sendto(message.encode(), (self.host, self.port))

    def stop(self):
        self.sock.close()

