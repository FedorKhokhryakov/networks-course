import socket
import argparse

def is_port_free(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        result = s.connect_ex((ip, port))
        return result != 0


def scan_ports(ip, start_port, end_port):
    print(f"Free ports on {ip} ({start_port}-{end_port}):")

    free_ports = []

    for port in range(start_port, end_port + 1):
        if is_port_free(ip, port):
            free_ports.append(port)
        else :
            print(f"Port {port} is not free")

    print(f"Found {len(free_ports)} free ports\n")
    #print(", ".join(map(str, free_ports)))


def main():
    parser = argparse.ArgumentParser(description="Network utility")

    parser.add_argument("--ip", type=str)
    parser.add_argument("--start", type=int)
    parser.add_argument("--end", type=int)

    args = parser.parse_args()

    if not (args.ip and args.start and args.end):
        print("Error: for scanning specify --ip --start --end")
        return

    scan_ports(args.ip, args.start, args.end)


if __name__ == "__main__":
    main()