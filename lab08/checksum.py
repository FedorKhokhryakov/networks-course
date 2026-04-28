def compute_checksum(data: bytes) -> int:
    if len(data) % 2 == 1:
        data += b'\x00'

    checksum = 0

    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        checksum += word

        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    checksum = ~checksum & 0xFFFF
    return checksum

def verify_checksum(data: bytes, checksum: int) -> bool:
    if len(data) % 2 == 1:
        data += b'\x00'

    total = 0

    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        total += word
        total = (total & 0xFFFF) + (total >> 16)

    total += checksum
    total = (total & 0xFFFF) + (total >> 16)

    return total == 0xFFFF

def tests():
    print("Test 1: correct data")
    data1 = b"Hello, world!!"
    checksum1 = compute_checksum(data1)
    print("Checksum:", hex(checksum1))
    print("Valid:", verify_checksum(data1, checksum1))
    print()

    print("Test 2: corrupted data")
    corrupted = bytearray(data1)
    corrupted[0] ^= 0x88
    print("Valid:", verify_checksum(corrupted, checksum1))
    print()

    print("Test 3: odd length data")
    data2 = b"ABC"
    checksum2 = compute_checksum(data2)
    print("Checksum:", hex(checksum2))
    print("Valid:", verify_checksum(data2, checksum2))


if __name__ == "__main__":
    tests()