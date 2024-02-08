from schnorr import *
from utilities import *


# 通过文件获得公私钥pem列表
def get_keys_pem(pem_file):
    df = pd.read_csv(pem_file)
    pk_pems = df['sig_pk']
    sk_pems = df['sig_sk']

    return list(pk_pems), list(sk_pems)


# 将公私钥pem列表转化为bytes列表
def keys_pem_to_bytes(pk_pems, sk_pems):
    pks_bytes = [pem_to_pk_bytes(pk_pem) for _ in pk_pems]
    sks_bytes = [pem_to_sk_bytes(sk_pem) for _ in sk_pems]

    return pks_bytes, sks_bytes


def ring_sing(pks, sig_key, msg):
    sig_pk, sig_sk = sig_key
    sig_pk_idx = pks.index(sig_pk)

    tees = [randsn() for _ in range(0, len(pks))]
    cees = [0 for _ in range(0, len(pks))]
    alpha = randsn()

    i = sig_pk_idx
    n = 0
    while n < len(pks):
        idx = i % len(pks)
        c = alpha if n == 0 else cees[idx - 1]
        cees[idx] = schnorr_calc(pks[idx], tees[idx], c, msg)
        n += 1
        i += 1

    alpha_gap = submodn(alpha, cees[sig_pk_idx - 1])
    tees[sig_pk_idx] = addmodn(tees[sig_pk_idx], mulmodn(sig_sk, alpha_gap))

    return pks, tees, cees[-1]
