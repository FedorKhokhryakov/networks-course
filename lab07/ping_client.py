import socket
import time
import sys

if len(sys.argv) != 3:
    print("Usage: ping_client.py <server_host> <server_port>")
    sys.exit(1)

SERVER_HOST = sys.argv[1]
SERVER_PORT = int(sys.argv[2])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1)

rtts = []
lost_packets = 0

print(f"Pinging {SERVER_HOST}:{SERVER_PORT}...\n")

for seq in range(10):
    send_time = time.time()
    message = f"Ping {seq+1} {send_time}"

    try:
        client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))

        response, _ = client_socket.recvfrom(1024)
        recv_time = time.time()

        rtt = recv_time - send_time
        rtts.append(rtt)

        print(f"Reply from {SERVER_HOST}: {response.decode()} RTT={rtt:.4f} sec")

    except socket.timeout:
        print("Request timed out")
        lost_packets += 1

print("\n--- Ping statistics ---")
sent = 10
received = sent - lost_packets
loss_percent = (lost_packets / sent) * 100

print(f"Packets: Sent = {sent}, Received = {received}, Lost = {lost_packets} ({loss_percent:.0f}% loss)")

if rtts:
    print(f"RTT min/avg/max = {min(rtts):.4f}/{sum(rtts)/len(rtts):.4f}/{max(rtts):.4f} sec")