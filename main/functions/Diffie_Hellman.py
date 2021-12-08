import random
from .Algoritms import evkl, exp_mod, modinv, Is_prime, Gen_prime


def Diffie_Hellman_gen_P_G():
    flag = 1
    while 1 == 1:
        q = Gen_prime(pow(10, 100))
        if Is_prime(2 * q + 1):
            p = 2 * q + 1
            abc = 0
            while 1 == 1:
                abc += 1
                g = random.randint(0, p - 1)
                if exp_mod(g, q, p) != 1:
                    return p, g


def Diffie_Hellman_gen(p, g):
    Xa = Gen_prime(p)
    Xb = Gen_prime(p)

    Ya = exp_mod(g, Xa, p)
    Yb = exp_mod(g, Xb, p)

    Zab = exp_mod(Yb, Xa, p)
    Zba = exp_mod(Ya, Xb, p)

    return Xa, Xb, Ya, Yb
