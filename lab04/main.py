import socket
import threading
import sys
import os
import hashlib

BUFF_SIZE = 1024
CACHE_DIR = "cache"
LOG_FILE = "proxy.log"
BLACKLIST_FILE = "blacklist.txt"

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def log(message):
    print(message)
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

def load_blacklist():
    if not os.path.exists(BLACKLIST_FILE):
        return set()
    with open(BLACKLIST_FILE) as f:
        ans = set()
        for line in f:
            line = line.strip()
            ans.add(line)
        return ans

BLACKLIST = load_blacklist()


def is_blocked(host):
    return any(b in host for b in BLACKLIST)


def get_cache_path(url):
    return os.path.join(CACHE_DIR, hashlib.md5(url.encode()).hexdigest())


def build_request(method, path, headers, host):
    req = f"{method} {path} HTTP/1.1\r\n"

    req += f"Host: {host}\r\n"

    for k, v in headers.items():
        if k.lower() not in ["host", "connection"]:
            req += f"{k}: {v}\r\n"

    req += "Connection: close\r\n"
    req += "\r\n"

    return req

def parse_request(request):
    lines = request.split("\r\n")
    method, url, _ = lines[0].split()

    headers = {}
    for line in lines[1:]:
        if ": " in line:
            k, v = line.split(": ", 1)
            headers[k] = v

    return method, url, headers


def connect_to_server(host, port=80):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s


def handle_client(client_socket):
    try:
        request = b""
        while b"\r\n\r\n" not in request:
            request += client_socket.recv(BUFF_SIZE)

        header_end = request.find(b"\r\n\r\n")
        headers_part = request[:header_end].decode()
        body = request[header_end + 4:]

        method, url, headers = parse_request(headers_part)

        if method.upper() == "POST":
            content_length = int(headers.get("Content-Length", 0))
            while len(body) < content_length:
                body += client_socket.recv(BUFF_SIZE)

        url = url.lstrip("/")

        if url.startswith("http://"):
            url = url[7:]

        host_port_path = url

        parts = host_port_path.split("/", 1)

        host_port = parts[0]
        path = "/" + parts[1] if len(parts) > 1 else "/"

        if ":" in host_port:
            host, port = host_port.split(":")
            port = int(port)
        else:
            host = host_port
            port = 80

        if is_blocked(host):
            response = "HTTP/1.1 403 Forbidden\r\nBlocked by proxy"
            client_socket.sendall(response.encode())
            log(f"[BLOCKED] {url}")
            client_socket.close()
            return

        cache_path = get_cache_path(url)
        cached_headers_path = cache_path + ".headers"

        use_cache = False

        if os.path.exists(cache_path):
            use_cache = True

        print(f"Connecting to {host}:{port}")
        server_socket = connect_to_server(host, port)
        print("connected to server!")

        if use_cache and method == "GET":
            headers_cond = ""

            if os.path.exists(cached_headers_path):
                with open(cached_headers_path) as f:
                    for line in f:
                        if line.startswith("Last-Modified"):
                            headers_cond += line
                        if line.startswith("ETag"):
                            headers_cond += line.replace("ETag", "If-None-Match")

            request_line = build_request(method, path, headers, host)
        else:
            request_line = build_request(method, path, headers, host)

        server_socket.sendall(request_line.encode() + body)

        response = b""
        while True:
            data = server_socket.recv(BUFF_SIZE)
            if not data:
                break
            response += data

        status_code = response.split(b"\r\n", 1)[0].decode().split()[1]

        if b"304 Not Modified" in response and use_cache:
            with open(cache_path, "rb") as f:
                cached_data = f.read()

            client_socket.sendall(cached_data)
            log(f"[CACHE HIT] {url}")
        else:
            client_socket.sendall(response)

            if method == "GET":
                with open(cache_path, "wb") as f:
                    f.write(response)

                headers_end = response.find(b"\r\n\r\n")
                if headers_end != -1:
                    with open(cached_headers_path, "wb") as f:
                        f.write(response[:headers_end])

            log(f"[FETCH] {url} -> {status_code}")

        client_socket.close()
        server_socket.close()

    except Exception as e:
        log(f"[ERROR] {e}")
        try:
            client_socket.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
        except:
            pass
        client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Need only one argument: <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)

    print(f"Proxy server running on port {port}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,))
        thread.start()