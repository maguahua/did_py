from past.builtins import long

from ring.curve25519 import *


def schnorr_calc(xG, s, e, message, point=None):
    assert isinstance(s, long)
    assert isinstance(e, long)
    assert isinstance(message, long)
    sG = multiply(point, s) if point else sbmul(s)
    kG = add(sG, multiply(xG, e))
    return hashs(xG[0], xG[1], kG[0], kG[1], message)
