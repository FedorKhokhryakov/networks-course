import os
import time
import struct
import socket
import argparse


ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0
ICMP_TIME_EXCEEDED = 11


def checksum(data):
    s = 0

    count_to = (len(data) // 2) * 2

    count = 0
    while count < count_to:
        this_val = data[count + 1] * 256 + data[count]
        s += this_val
        s &= 0xffffffff
        count += 2

    if count_to < len(data):
        s += data[-1]
        s &= 0xffffffff

    s = (s >> 16) + (s & 0xffff)
    s += (s >> 16)

    answer = ~s
    answer &= 0xffff

    answer = socket.htons(answer)

    return answer


def build_packet(packet_id, sequence):
    header = struct.pack(
        "!BBHHH",
        ICMP_ECHO_REQUEST,
        0,
        0,
        packet_id,
        sequence
    )

    payload = struct.pack("!d", time.time())

    cs = checksum(header + payload)

    header = struct.pack(
        "!BBHHH",
        ICMP_ECHO_REQUEST,
        0,
        cs,
        packet_id,
        sequence
    )

    return header + payload


def resolve_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return None


def parse_icmp_reply(packet):
    ip_header_len = (packet[0] & 0x0F) * 4

    icmp_header = packet[ip_header_len:ip_header_len + 8]

    if len(icmp_header) < 8:
        return None, None

    icmp_type, code, cs, p_id, seq = struct.unpack(
        "!BBHHH",
        icmp_header
    )

    return icmp_type, p_id


def traceroute(host, max_hops=30, timeout=3, probes=3):
    try:
        destination_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"Cannot resolve host: {host}")
        return

    print(f"Tracing route to {host} [{destination_ip}]")
    print()

    packet_id = os.getpid() & 0xFFFF

    for ttl in range(1, max_hops + 1):
        print(f"{ttl:2d} ", end="\t")

        current_addr = None
        current_name = None
        reached_destination = False

        for probe in range(probes):
            try:
                sock = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_RAW,
                    socket.IPPROTO_ICMP
                )
            except PermissionError:
                print("\nRun program as root.")
                return

            sock.setsockopt(
                socket.IPPROTO_IP,
                socket.IP_TTL,
                ttl
            )

            sock.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_RCVBUF,
                65535
            )

            sock.settimeout(timeout)

            sequence = ttl * probes + probe

            packet = build_packet(packet_id, sequence)

            start_time = time.time()

            try:
                sock.sendto(packet, (destination_ip, 0))

                recv_packet, addr = sock.recvfrom(65535)

                end_time = time.time()

                rtt = (end_time - start_time) * 1000

                current_addr = addr[0]

                if current_name is None:
                    current_name = resolve_hostname(current_addr)

                icmp_type, reply_id = parse_icmp_reply(recv_packet)

                if reply_id == packet_id:
                    if icmp_type == ICMP_ECHO_REPLY:
                        reached_destination = True

                print(f"{rtt:.2f} ms ", end="\t")

            except socket.timeout:
                print("*\t", end="\t")

            finally:
                sock.close()

        if current_addr:
            if current_name:
                print(f"{current_name} [{current_addr}]")
            else:
                print(current_addr)
        else:
            print("Request timed out")

        if current_addr == destination_ip or reached_destination:
            print("\nTrace complete.")
            break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("-m", "--max-hops", type=int, default=30)
    parser.add_argument("-t", "--timeout", type=int, default=3)
    parser.add_argument("-p", "--probes", type=int, default=3)

    args = parser.parse_args()

    traceroute(
        args.host,
        max_hops=args.max_hops,
        timeout=args.timeout,
        probes=args.probes
    )

if __name__ == "__main__":
    main()