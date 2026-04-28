import socket
import random
import argparse
from checksum import verify_checksum, compute_checksum

LOSS_PROB = 0.3

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=9999)
    parser.add_argument("--outfile", default="received.txt")

    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", args.port))

    print(f"Server started at 0.0.0.0:{args.port}")

    expected_seq = 0

    with open(args.outfile, "wb") as f:
        while True:
            data, addr = sock.recvfrom(1024)

            if random.random() < LOSS_PROB:
                print("Packet lost")
                continue

            pkt_type = data[0]
            seq = data[1]
            recv_checksum = int.from_bytes(data[2:4], "big")
            payload = data[4:]

            if not verify_checksum(bytes([pkt_type, seq]) + payload, recv_checksum):
                print("Corrupted packet → drop")
                continue

            if pkt_type == 0:
                print(f"Received DATA seq={seq}")

                if seq == expected_seq:
                    f.write(payload)
                    f.flush()
                    expected_seq = 1 - expected_seq
                    print("Accepted")
                else:
                    print("Duplicate packet")

                header = bytes([1, seq])
                checksum = compute_checksum(header)
                ack = header + checksum.to_bytes(2, "big")

                if random.random() < LOSS_PROB:
                    print("ACK lost")
                    continue

                sock.sendto(ack, addr)
                print(f"ACK sent seq={seq}")


if __name__ == "__main__":
    main()