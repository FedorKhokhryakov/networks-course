import socket
import random
import argparse
from checksum import compute_checksum, verify_checksum

LOSS_PROB = 0.3
CHUNK_SIZE = 512

def make_packet(pkt_type, seq, payload=b""):
    header = bytes([pkt_type, seq])
    checksum = compute_checksum(header + payload)
    return header + checksum.to_bytes(2, "big") + payload

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9999)
    parser.add_argument("--timeout", type=float, default=1.0)
    parser.add_argument("--infile", default="input.txt")

    args = parser.parse_args()

    server_addr = (args.host, args.port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(args.timeout)

    seq = 0

    with open(args.infile, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break

            while True:
                packet = make_packet(0, seq, chunk)

                if random.random() < LOSS_PROB:
                    print("Packet lost")
                elif random.random() < 0.1:
                    packet = bytearray(packet)
                    packet[5] ^= 0x67
                    #packet = bytes(packet)
                    print("Packet corrupted (simulated)")
                else:
                    sock.sendto(packet, server_addr)
                    print(f"Sent DATA seq={seq}")

                try:
                    ack, _ = sock.recvfrom(1024)

                    if random.random() < LOSS_PROB:
                        print("ACK lost after receive")
                        continue

                    ack_type = ack[0]
                    ack_seq = ack[1]
                    recv_checksum = int.from_bytes(ack[2:4], "big")

                    if not verify_checksum(bytes([ack_type, ack_seq]), recv_checksum):
                        print("Corrupted ACK → ignore")
                        continue

                    if ack_type == 1 and ack_seq == seq:
                        print(f"Received ACK seq={ack_seq}")
                        seq = 1 - seq
                        break

                except socket.timeout:
                    print(f"Timeout ({args.timeout}s) -> retransmit")

    print("File sent successfully")


if __name__ == "__main__":
    main()