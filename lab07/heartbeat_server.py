import socket
import time

HOST = "0.0.0.0"
PORT = 13000
TIMEOUT = 4

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"Heartbeat Server started at {HOST}:{PORT}")

clients = {}

while True:
    server_socket.settimeout(1)

    try:
        message, client_address = server_socket.recvfrom(1024)
        curr_time = time.time()

        seq, timestamp = message.decode().split()
        timestamp = float(timestamp)

        delay = curr_time - timestamp

        print(f"[HEARTBEAT] {client_address} seq={seq} delay={delay:.4f}s")

        clients[client_address] = curr_time

    except socket.timeout:
        pass

    now = time.time()
    for client, last_time in list(clients.items()):
        if now - last_time > TIMEOUT:
            print(f"[TIMEOUT] Client {client} doesn't answered (>{TIMEOUT} seconds)")
            del clients[client]