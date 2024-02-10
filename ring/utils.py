import binascii
import sys
from functools import reduce
from hashlib import sha256
from os import urandom
from random import randint


def quote(x):
    return '"' + str(x) + '"'


def quotemany(*x):
    return ','.join(map(quote, x))


def quotelist(x):
    return '[' + quotemany(*x) + ']'


safe_ord = ord if sys.version_info.major == 2 else lambda x: x if isinstance(x, int) else ord(x)


def bytes_to_int(x):
    return reduce(lambda o, b: (o << 8) + safe_ord(b), [0] + list(x))


def packl(lnum):
    if lnum == 0:
        return b'\0'
    s = hex(lnum)[2:].rstrip('L')
    if len(s) & 1:
        s = '0' + s
    return binascii.unhexlify(s)


int_to_big_endian = packl


def zpad(x, l):
    return b'\x00' * max(0, l - len(x)) + x


def tobe256(v):
    return zpad(int_to_big_endian(v), 32)


def hashs(*x):
    data = b''.join(map(tobe256, x))
    return bytes_to_int(sha256(data).digest())


def randb256():
    return urandom(32)


b = 256
q = 2 ** 255 - 19
n = l = 2 ** 252 + 27742317777372353535851937790883648493
byte_length = (252 + 7) // 8

def hashsn(*x):
    return hashs(*x) % n


def hashpn(*x):
    return hashsn(*[item for sublist in x for item in sublist])


def randsn():
    return randint(1, n - 1)


def inv(x):
    return pow(x, q - 2, q)


def addmodn(x, y):
    return (x + y) % n


def mulmodn(x, y):
    return (x * y) % n


def submodn(x, y):
    return (x - y) % n


def h1(s):
    return bytes_to_int(sha256(s).digest()) % n


d = -121665 * inv(121666)
I = pow(2, (q - 1) // 4, q)


def xrecover(y):
    xx = (y * y - 1) * inv(d * y * y + 1)
    x = pow(xx, (q + 3) // 8, q)
    if (x * x - xx) % q != 0: x = (x * I) % q
    if x % 2 != 0: x = q - x
    return x


By = 4 * inv(5)
Bx = xrecover(By)
B = [Bx % q, By % q]
G = B
