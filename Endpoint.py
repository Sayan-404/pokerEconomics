import socket
import json

# Configure the host and port to listen on
HOST = "127.0.0.1"  # Localhost
PORT = 5005
BUFFER_SIZE = 4096  # Increased buffer size for larger data packets

# Set up a TCP socket to receive data
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Use TCP instead of UDP
sock.bind((HOST, PORT))

# Listen for incoming connections (max 1 client in this case)
sock.listen(1)
print("Waiting for a connection...")

# Accept the incoming connection
connection, client_address = sock.accept()
print(f"Connection established with {client_address}")

last_received_data = None  # Variable to store the last received data
data_buffer = ""  # Accumulate the data here

try:
    while True:
        # Receive data from the socket
        data = connection.recv(BUFFER_SIZE)

        if not data:
            # No more data from the client, break the loop
            break

        # Accumulate the data in a buffer until the full message is received
        data_buffer += data.decode()

        # Check if the entire JSON object is received (based on your JSON structure)
        try:
            engine_data = json.loads(data_buffer)
            last_received_data = engine_data  # Update last_received_data with the most recent data
            data_buffer = ""  # Reset buffer after successfully decoding
            print(f"Received data: {engine_data}")

        except json.JSONDecodeError:
            # If the data is incomplete, keep accumulating
            continue

except KeyboardInterrupt:
    print("Data reception interrupted by user.")

finally:
    # Save the last received data to a file before closing the connection
    if last_received_data:
        with open("last_received_data.json", "w") as f:
            json.dump(last_received_data, f, indent=4)
        print("Last received data saved to 'last_received_data.json'.")

    # Close the connection and the socket
    connection.close()
    sock.close()
    print("Connection and socket closed.")
