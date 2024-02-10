from schnorr import *


def aosring_randkeys(n=20):
    skeys = [randsn() for _ in range(0, n)]
    pkeys = [sbmul(sk) for sk in skeys]
    return pkeys, skeys


def aosring_sign(pkeys, mypair, tees=None, alpha=None, message=None):
    assert len(pkeys) > 0
    message = message or hashpn(*pkeys)
    mypk, mysk = mypair
    myidx = pkeys.index(mypk)

    tees = tees or [randsn() for _ in range(0, len(pkeys))]
    cees = [0 for _ in range(0, len(pkeys))]
    alpha = alpha or randsn()

    i = myidx
    n = 0
    while n < len(pkeys):
        idx = i % len(pkeys)
        c = alpha if n == 0 else cees[idx - 1]
        cees[idx] = schnorr_calc(pkeys[idx], tees[idx], c, message)
        n += 1
        i += 1

    # Then close the ring, which proves we know the secret for one ring item
    # TODO: split into schnorr_alter
    alpha_gap = submodn(alpha, cees[myidx - 1])
    tees[myidx] = addmodn(tees[myidx], mulmodn(mysk, alpha_gap))

    return pkeys, tees, cees[-1]


def aosring_check(pkeys, tees, seed, message=None):
    assert len(pkeys) > 0
    assert len(tees) == len(pkeys)
    message = message or hashpn(*pkeys)
    c = seed
    for i, pkey in enumerate(pkeys):
        c = schnorr_calc(pkey, tees[i], c, message)
    return c == seed


# 一个签名的小demo
if __name__ == "__main__":
    # 这里随便选一个整数作为消息签名，aos基于schnorr，签名的消息需要是整数形式，如果不会变可以参考使用h1
    msg = 'my test data'

    # 生成了3对key
    pks, sks = aosring_randkeys(3)
    print('pks:\n', pks)
    print('sks:\n', sks)

    sk = sks[1]
    pk = pks[1]
    mykey = (pk, sk)

    sk_bytes = sk

    # 签名时提供所有的公钥，自己的公私钥对，以及消息m
    # sig=aosring_sign(pks,mykey, message=msg)
    # 验证签名，应该通过
    # print(aosring_check(*sig, message=msg))

    # 随便换一下消息，不通过
    # msg = randsn()
    # print(aosring_check(*sig, message=msg))
