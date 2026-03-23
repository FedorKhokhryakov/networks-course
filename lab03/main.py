import socket
import sys
import os
import threading


def handle(conn, semaphore):
    with semaphore:
        data = conn.recv(1024).decode()
        print("\nrequest:\n", data)

        try:
            first_line = data.splitlines()[0]
            method, path, _ = first_line.split()
            file = path.lstrip("/")
        except:
            conn.close()
            return

        answer = b""
        print(file)
        if os.path.exists(file):
            with open(file, "rb") as f:
                body = f.read()

            answer += b"HTTP/1.1 200 OK\r\n"
            answer += b"Content-Length: " + str(len(body)).encode() + b"\r\n"
            answer += b"Content-Type: text/html\r\n\r\n"
            answer += body
        else:
            body = b"<h1>404 Not Found</h1>"
            answer = b"HTTP/1.1 404 Not Found\r\n"
            answer += b"Content-Length: " + str(len(body)).encode() + b"\r\n"
            answer += b"Content-Type: text/html\r\n\r\n"
            answer += body

        conn.sendall(answer)
        conn.close()

def main():
    server_port = int(sys.argv[1])
    concurrency_level = int(sys.argv[2])
    semaphore = threading.Semaphore(concurrency_level)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', server_port))
    s.listen(1)
    print("server listening on port", server_port)

    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle, args=(conn, semaphore))
        thread.start()

if __name__ == '__main__':
    main()