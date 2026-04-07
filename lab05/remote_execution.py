import socket
import subprocess


HOST = "0.0.0.0"
PORT = 5000

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    print("Server started...")

    while True:
        conn, addr = server.accept()
        print("Connected:", addr)

        cmd = conn.recv(1024).decode()
        print("Command:", cmd)

        try:
            result = subprocess.check_output(
                cmd, shell=True, stderr=subprocess.STDOUT
            )
        except subprocess.CalledProcessError as e:
            result = e.output

        conn.send(result)
        conn.close()


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", PORT))

    cmd = input("Enter command: ")
    client.send(cmd.encode())

    result = client.recv(4096).decode()
    print(result)

    client.close()

if __name__ == "__main__":
    mode = int(input("choose:\n1 - server\n2 - client:\n"))

    if mode == 1:
        start_server()
    else:
        start_client()