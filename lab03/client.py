import socket
import sys

def main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    file = sys.argv[3]

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    request = f"GET /{file} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    client.send(request.encode())

    response = b""
    while True:
        data = client.recv(1024)
        if not data:
            break
        response += data

    print(response.decode(errors="ignore"))
    client.close()


if __name__ == "__main__":
    main()