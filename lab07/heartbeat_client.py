import socket
import time
import sys

if len(sys.argv) != 3:
    print("Usage: heartbeat_client.py <server_host> <server_port>")
    sys.exit(1)

SERVER_HOST = sys.argv[1]
SERVER_PORT = int(sys.argv[2])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

seq = 1

print("Heartbeat client started")

while True:
    timestamp = time.time()
    message = f"{seq} {timestamp}"

    client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))
    print(f"Sent heartbeat seq={seq}")

    seq += 1
    time.sleep(1)