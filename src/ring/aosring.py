from src.ring.schnorr import *


# 环签名参数（pkList, 本地GM公私钥对，None,None，vc_int）
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


# 环签名验证，前三个就是signature
def aosring_check(pkeys, tees, seed, message=None):
    assert len(pkeys) > 0
    assert len(tees) == len(pkeys)
    # print(message)
    message = message
    c = seed
    for i, pkey in enumerate(pkeys):
        c = schnorr_calc(pkey, tees[i], c, message)
    return c == seed


# 一个签名的小demo
if __name__ == "__main__":
    # 这里随便选一个整数作为消息签名，aos基于schnorr，签名的消息需要是整数形式，如果不会变可以参考使用h1
    msg = 123456

    from utilities import gen_key, tuple_to_bytes

    #
    # keys_list = [[gen_key() for _ in range(length)] for length in range(1, 51)]
    # elapse_time_list = []
    #
    # for i in range(50):
    #     pk_list = [key_pair_list[0] for key_pair_list in keys_list[i]]
    #     keypair = random.choice(keys_list[i])  # 随机在里面选一个签名者
    #     start_time = time.time()
    #     signature = aosring_sign(pk_list, keypair, message=msg)
    #     bytes_sig = tuple_to_bytes(signature)
    #     end_time = time.time()
    #     elapse_time = end_time - start_time
    #     elapse_time_list.append(elapse_time)
    #
    #     print(i, elapse_time)
    #
    # df = pd.DataFrame()
    # df['elapse_time'] = elapse_time_list
    # df.to_csv('ring sig time.csv')

    keys = [gen_key() for _ in range(3)]

    pks = [key[0] for key in keys]

    mykey = keys[0]
    print(mykey)

    # 签名时提供所有的公钥，自己的公私钥对，以及消息m
    sig = aosring_sign(pks, mykey, message=msg)
    bytes_sig = tuple_to_bytes(sig)

    # 验证签名，应该通过
    print(aosring_check(*sig, message=msg))

    # 随便换一下消息，不通过
    msg = 234567
    print(aosring_check(*sig, message=msg))
