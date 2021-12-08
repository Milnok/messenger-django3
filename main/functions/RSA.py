import random
from .Algoritms import evkl, exp_mod, modinv, Is_prime, Gen_prime


def RSA_gen_PQE():
    p = Gen_prime(10 ** 100)
    q = Gen_prime(10 ** 100)
    return p, q


def RSA_gen(p, q):
    p, q = int(p), int(q)
    fi = (p - 1) * (q - 1)
    n = p * q
    while True:
        e = Gen_prime(fi - 1)
        if evkl(fi, e) and n % e != 0 and modinv(e, fi) is not None:
            d = modinv(e, fi)
            return e, d, n


def RSA_shifr(text, e, n, file):
    if file:
        ifst = open(text, "rb").read()
        text = ifst
    if not file:
        text1 = []
        for i in text:
            text1.append(ord(i))
        text = text1
    otv = ""
    for i in text:
        if i > n:
            return None
        otv += str(exp_mod(i, e, n)) + " "
    otv = otv[:-1]
    if file:
        ofst = open("shifr.txt", "w")
        ofst.write(otv)
    if not file:
        return otv


def RSA_deshifr(text, d, n, filetype, file):
    if file:
        ifst = open("shifr.txt", "r").read()
        ofst = open("output." + filetype, "wb")
        text = ifst
    chisla = text.split(" ")
    otv = ""
    for i in chisla:
        if file:
            ofst.write(bytes([exp_mod(int(i), d, n)]))
        if not file:
            otv += chr(exp_mod(int(i), d, n))
    if not file:
        return otv

if __name__ == '__main__':
    prime_P, prime_Q = RSA_gen_PQE()
    pen_key, secret_key, none = RSA_gen(prime_P, prime_Q)
