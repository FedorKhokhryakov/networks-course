import socket
import time


PORT = 5001

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        message = time.ctime()
        sock.sendto(message.encode(), ("255.255.255.255", PORT))
        print("Sent:", message)
        time.sleep(1)


def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", PORT))

    while True:
        data, addr = sock.recvfrom(1024)
        print("Time:", data.decode())


if __name__ == "__main__":
    mode = int(input("choose:\n1 - server\n2 - client:\n"))

    if mode == 1:
        start_server()
    else:
        start_client()