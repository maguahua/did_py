import csv
import hashlib
import json

import base58
import numpy as np
import pandas as pd
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey


# 根据省份文件生成省份元组供之后使用
def gen_provinces(province_file):
    provinces_set = set()

    with open(province_file, 'r', encoding='gbk', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if row:
                province = row[2]
                provinces_set.add(province)
        provinces_tuple = tuple(provinces_set)

    return provinces_tuple


# 使用ed25519生成一对公私钥对（不序列化）
def gen_key_pair():
    # 私钥
    sk = ed25519.Ed25519PrivateKey.generate()
    # 公钥
    pk = sk.public_key()
    return pk, sk


# 根据一个公钥生成一个DID
def gen_did(province, pk):
    # 对公钥进行sha256哈希
    pk_sha256 = hashlib.sha256(pk_to_bytes(pk))
    did_msi = pk_sha256.hexdigest()
    # 生成did
    did = f'did:grid:{province}:{did_msi}'

    return did


# region:公私钥对象、字节串、字符串互相转换
def pk_to_bytes(pk):
    pk_bytes = pk.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    return pk_bytes


def sk_to_bytes(sk):
    sk_bytes = sk.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    return sk_bytes


def bytes_to_pk(pk_bytes):
    pk = Ed25519PublicKey.from_public_bytes(pk_bytes)
    return pk


def bytes_to_sk(sk_bytes):
    sk = Ed25519PrivateKey.from_private_bytes(sk_bytes)
    return sk


def pk_to_pem(pk):
    pk_pem = pk.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pk_pem


def sk_to_pem(sk):
    sk_pem = sk.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return sk_pem


def pem_to_pk(pk_pem):
    if isinstance(pk_pem, str):
        pk_pem = pk_pem.encode('utf-8')
    pk = serialization.load_pem_public_key(pk_pem, backend=default_backend())
    return pk


def pem_to_sk(sk_pem):
    if isinstance(sk_pem, str):
        sk_pem = sk_pem.encode('utf-8')
    sk = serialization.load_pem_private_key(sk_pem, None, backend=default_backend())
    return sk


def pem_to_pk_bytes(pk_pem):
    pk = pem_to_pk(pk_pem)
    pk_bytes = pk_to_bytes(pk)
    return pk_bytes


def pem_to_sk_bytes(sk_pem):
    sk = pem_to_sk(sk_pem)
    sk_bytes = sk_to_bytes(sk)
    return sk_bytes


def pk_bytes_to_pem(pk_bytes):
    pk = bytes_to_pk(pk_bytes)
    pk_pem = pk_to_pem(pk)
    return pk_pem


def sk_bytes_to_pem(sk_bytes):
    sk = bytes_to_sk(sk_bytes)
    sk_pem = sk_to_pem(sk)
    return sk_pem


# endregion

def pk_to_base58(pk_bytes):
    multikey = 'z' + base58.b58encode(pk_bytes).decode()
    return multikey


def gen_did_doc(did, pk_bytes):
    did_doc = {
        "@context": [
            "https://www.w3.org/ns/did/v1",
            "https://w3id.org/security/data-integrity/v1"
        ],
        "id": did,
        "verificationMethod": [{
            "id": did,
            "type": "Multikey",
            "controller": did,
            "publicKeyMultibase": pk_to_base58(pk_bytes)
        }]
    }
    return json.dumps(did_doc, indent=4)


def add_new_column(file, new_col_name):
    df = pd.read_csv(file)
    df[new_col_name] = np.nan
    df.to_csv(file, index=False)


if __name__ == '__main__':
    '''
    生成了一对公私钥对，转化为bytes格式
    生成该公私钥对的pem序列格式
    将两个pem转化为公私钥对的原始形式，再转化为bytes形式
    最终发现，原始公私钥对的bytes和由pem转化为公私钥对再转化为bytes内容相同
    值得注意的是，新生成的原始公私钥对对象和最开始的原始公私钥对对象是不同的
    由此说明，原始形式存储的是内存地址，但内容是相同的
    '''
    pk, sk = gen_key_pair()
    print('pk:', pk)
    print('sk:', sk)

    pk_bytes = pk_to_bytes(pk)
    sk_bytes = sk_to_bytes(sk)
    print('pk_bytes:', pk_bytes)
    print('sk_bytes:', sk_bytes)

    pk_pem = pk_to_pem(pk)
    sk_pem = sk_to_pem(sk)
    print('pk_pem:', pk_pem)
    print('sk_pem:', sk_pem)

    new_pk = pem_to_pk(pk_pem)
    new_sk = pem_to_sk(sk_pem)
    print('pk_new:', new_pk)
    print('sk_new:', new_sk)

    new_pk_bytes = pk_to_bytes(new_pk)
    new_sk_bytes = sk_to_bytes(new_sk)
    print('new_pk_bytes:', new_pk_bytes)
    print('new_sk_bytes:', new_sk_bytes)

    new_pk_pem = pk_bytes_to_pem(new_pk_bytes)
    new_sk_pem = sk_bytes_to_pem(new_sk_bytes)
    print('new_pk_pem:', new_pk_pem)
    print('new_sk_pem:', new_sk_pem)

    print('new_pk_bytes == pk_bytes:', new_pk_bytes == pk_bytes)
    print('new_sk_bytes == sk_bytes:', new_sk_bytes == sk_bytes)
