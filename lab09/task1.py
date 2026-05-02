import socket
import psutil

def get_network_info():
    addrs = psutil.net_if_addrs()

    for interface, addr_list in addrs.items():
        for addr in addr_list:
            if addr.family == socket.AF_INET:
                print(f"Interface: {interface}")
                print(f"  IP Address : {addr.address}")
                print(f"  Netmask    : {addr.netmask}")
                print()

if __name__ == "__main__":
    get_network_info()