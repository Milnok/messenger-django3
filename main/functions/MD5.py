import math
from bitarray import bitarray

text = 'md5'


def to_bit(text: str):
    otv = ''
    text = text.encode()
    for i in text:
        otv += bin(i)[2:].zfill(8)
    return otv


def bit512_to_list_int(block512):
    X = []
    bitArray = bitarray(block512)
    for i in range(len(bitArray) // 32):
        tmp = bitArray[:32]
        X.append(int.from_bytes(tmp.tobytes(), byteorder="little"))
        bitArray = bitArray[32:]
    return X


def FuncF(X, Y, Z):
    return (X & Y) | (~X & Z)


def FuncG(X, Y, Z):
    return (X & Z) | (Y & ~Z)


def FuncH(X, Y, Z):
    return X ^ Y ^ Z


def FuncI(X, Y, Z):
    return Y ^ (X | ~Z)


def add_length(text, file):
    bit_text = ''
    if file:
        ifst = open(text, 'rb').read()
        for i in ifst:
            bit_text += bin(i)[2:].zfill(8)
    else:
        bit_text = to_bit(text)
    bit_strk = bit_text + '1'
    while len(bit_strk) % 512 != 448:
        bit_strk += '0'
    lengthBin = bin(len(bit_text) % pow(2, 64))[2:].zfill(64)
    lengthBitArray = bitarray()
    lengthBitArray.extend(lengthBin)
    X = int.from_bytes(lengthBitArray.tobytes(), byteorder="little")
    bit_strk += bin(X)[2:].zfill(64)
    return bit_strk


def obrabotka_texta(int_list):
    A0 = 0x67452301
    B0 = 0xEFCDAB89
    C0 = 0x98BADCFE
    D0 = 0x10325476
    A, B, C, D = A0, B0, C0, D0
    T = [int(pow(2, 32) * abs(math.sin(i + 1))) for i in range(64)]
    for one_block in int_list:
        A, B, C, D = obrabotka_512block(one_block, T, A, B, C, D)
    try:
        return A, B, C, D
    except:
        return None


def obrabotka_512block(int_512bit, T, A0, B0, C0, D0):
    A, B, C, D = A0, B0, C0, D0
    for i in range(4 * 16):
        if 0 <= i <= 15:
            k = i
            s = [7, 12, 17, 22]
            temp = FuncF(B, C, D)
        elif 16 <= i <= 31:
            k = ((5 * i) + 1) % 16
            s = [5, 9, 14, 20]
            temp = FuncG(B, C, D)
        elif 32 <= i <= 47:
            k = ((3 * i) + 5) % 16
            s = [4, 11, 16, 23]
            temp = FuncH(B, C, D)
        elif 48 <= i <= 63:
            k = (7 * i) % 16
            s = [6, 10, 15, 21]
            temp = FuncI(B, C, D)

        temp = (temp + int_512bit[k]) % pow(2, 32)
        temp = (temp + T[i]) % pow(2, 32)
        temp = (temp + A) % pow(2, 32)
        temp = (temp << s[i % 4]) | (temp >> (32 - s[i % 4]))
        temp = (temp + B) % pow(2, 32)

        A = D
        D = C
        C = B
        B = temp

    A = (A0 + A) % pow(2, 32)
    B = (B0 + B) % pow(2, 32)
    C = (C0 + C) % pow(2, 32)
    D = (D0 + D) % pow(2, 32)

    return A, B, C, D


def MD5_hash(text, file: bool):
    int_list = []
    bit_strk = add_length(text, file)
    for i in range(len(bit_strk) // 512):
        int_list.append(bit512_to_list_int(bit_strk[i * 512:(i + 1) * 512]))
    A, B, C, D = obrabotka_texta(int_list)

    tmp = bitarray(endian="big")
    tmp.extend(bin(A)[2:].zfill(32))
    tmp.extend(bin(B)[2:].zfill(32))
    tmp.extend(bin(C)[2:].zfill(32))
    tmp.extend(bin(D)[2:].zfill(32))
    res = ''
    for i in range(4):
        res += str(hex(int.from_bytes(tmp[:32].tobytes(), byteorder="little"))[2:]).zfill(8)
        tmp = tmp[32:]
    return res


if __name__ == '__main__':
    print(MD5_hash('Text.txt', True))
    print(MD5_hash(text, False))
