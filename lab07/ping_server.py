import socket
import random

HOST = "0.0.0.0"
PORT = 12000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"UDP Ping Server started at {HOST}:{PORT}")

while True:
    message, client_address = server_socket.recvfrom(1024)

    if random.random() > 0.8:
        print(f"[LOSS] Packet from {client_address} is lost")
        continue

    modified_message = message.decode().upper()

    print(f"[RECV] {client_address}: {message.decode()}")
    server_socket.sendto(modified_message.encode(), client_address)