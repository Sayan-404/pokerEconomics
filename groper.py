import socket
import json

# Configure the host and port to listen on
HOST = "127.0.0.1"  # Localhost
PORT = 5005
BUFFER_SIZE = 4096  # Increased buffer size for larger data packets

# Set up a UDP socket to receive data
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print("Listening for engine data...")

try:
    while True:
        # Receive data from the socket
        data, addr = sock.recvfrom(BUFFER_SIZE)
        
        # Decode and parse the JSON data
        message = data.decode()
        engine_data = json.loads(message)
        
        # Print the received data
        print(f"Received data: {engine_data}")

except KeyboardInterrupt:
    print("Data reception interrupted by user.")

finally:
    # Close the socket
    sock.close()
    print("Socket closed.")
