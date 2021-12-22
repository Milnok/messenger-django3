from .MD5 import MD5_hash
from .RSA import RSA_shifr, RSA_deshifr
from .DES import codeDES
from .Diffie_Hellman import Diffie_Hellman_gen
from .Algoritms import exp_mod
from messenger.settings import server_secret_key, server_open_key, server_N, DH_P, DH_G


def client_shifr(message: str, Yb: int, Xa: int, open_key, N):
    message_hash = MD5_hash(message, False)  # Клиент
    shifr_hash = RSA_shifr(message_hash, open_key, N, False)  # Клиент
    shifr_message = codeDES(message.encode(), True, exp_mod(Yb, Xa, DH_P))  # Клиент
    return shifr_hash, shifr_message


def server_rasshifr(shifr_hash: str, shifr_message: str, Xb: int, Ya: int, secret_key, N):
    rasshifr_hash = RSA_deshifr(shifr_hash, secret_key, N, False, False)  # Сервер
    rasshifr_message = codeDES(shifr_message, False, exp_mod(Ya, Xb, DH_P)).decode()  # Сервер
    message_hash = MD5_hash(rasshifr_message, False)  # Сервер
    if message_hash == rasshifr_hash:
        return rasshifr_message
    else:
        return Exception


def from_client_to_server(message: str):
    Xa, Xb, Ya, Yb = Diffie_Hellman_gen(DH_P,
                                        DH_G)  # Сервер и клиент (Каждый свой ключ) А-сервер, Б-клиент, X-закрытый, Y-открытый
    shifr_hash, shifr_message = client_shifr(message, Yb, Xa, server_open_key, server_N)  # Клиент
    rasshifr_message = server_rasshifr(shifr_hash, shifr_message, Xb, Ya, server_secret_key, server_N)  # Сервер
    return rasshifr_message


def from_server_to_client(messages: set, keys):
    all_messages = []
    Xa, Xb, Ya, Yb = Diffie_Hellman_gen(DH_P,
                                        DH_G)  # Сервер и клиент (Каждый свой ключ) А-сервер, Б-клиент, X-закрытый, Y-открытый
    for obj in messages:
        shifr_hash, shifr_message = client_shifr(obj.text, Yb, Xa, int(keys.open_key), int(keys.n))  # Сервер
        rasshifr_message = server_rasshifr(shifr_hash, shifr_message, Xb, Ya, int(keys.secret_key), int(keys.n))  # Клиент
        all_messages.append(rasshifr_message)
    return all_messages


if __name__ == '__main__':
    from_client_to_server('Как дела вообще')
