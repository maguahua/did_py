import csv
import hashlib
import json

import base58
import numpy as np
import pandas as pd

from src.ring import randsn, sbmul


# 根据这个方法生成包含所有省份的元组，这个元组中只包含省份，为之后生成省份信息做铺垫
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


# 生成一个字典，字典的键是省份，值是省份对应的did
def get_province_did(gms_data_filename):
    df = pd.read_csv(gms_data_filename)
    province = df['province']
    did = df['did']
    gms_province_did = pd.Series(did.values, index=province).to_dict()
    return gms_province_did


# 生成一对公私钥对
def gen_key():
    sk = randsn()
    pk = sbmul(sk)
    return pk, sk


# 单个大数和字节串互相转换
def to_bytes(big_num) -> bytes:
    big_num_str = str(big_num) if type(big_num) == int else big_num
    big_num_bytes = big_num_str.encode('utf-8')
    return big_num_bytes


def to_big_num(big_num_bytes: bytes) -> int:
    big_num_str = big_num_bytes.decode('utf-8')
    big_num = int(big_num_str)
    return big_num


# 大数元组和字节串相互转换
def tuple_to_bytes(big_num_tuple: tuple) -> bytes:
    str_joined = tuple_to_str(big_num_tuple)
    str_bytes = str_joined.encode('utf-8')
    return str_bytes


def bytes_to_tuple(big_num_bytes: bytes) -> tuple:
    big_num_str = big_num_bytes.decode('utf-8')
    big_num = str_to_tuple(big_num_str)
    return big_num


# 大数元组和字符串互相转换
def tuple_to_str(big_num_tuple: tuple) -> str:
    big_num_str_list = [str(num) for num in big_num_tuple]
    big_num_str = ','.join(big_num_str_list)
    return big_num_str


def str_to_tuple(big_num_str: str) -> tuple:
    big_num_str = big_num_str.strip("()")
    big_num_str_list = big_num_str.split(',')
    big_num_tuple = tuple(int(num) for num in big_num_str_list)
    return big_num_tuple


def str_sig_to_tuple(str_sig: str) -> tuple:
    result = eval(str_sig)

    pk_list, tees, cee = result
    tuple_sig = (pk_list, tees, cee)
    return tuple_sig


# 根据一个公钥生成一个DID
def gen_did(province, pk: tuple):
    # 对公钥进行sha256哈希
    pk_sha256 = hashlib.sha256(tuple_to_bytes(pk))
    did_msi = pk_sha256.hexdigest()
    # 生成did
    did = f'did:grid:{province}:{did_msi}'

    return did


# # region:公私钥对象、字节串、字符串互相转换
# def pk_to_bytes(pk):
#     pk_bytes = pk.public_bytes(
#         encoding=serialization.Encoding.Raw,
#         format=serialization.PublicFormat.Raw
#     )
#     return pk_bytes
#
#
# def sk_to_bytes(sk):
#     sk_bytes = sk.private_bytes(
#         encoding=serialization.Encoding.Raw,
#         format=serialization.PrivateFormat.Raw,
#         encryption_algorithm=serialization.NoEncryption()
#     )
#     return sk_bytes
#
#
# def bytes_to_pk(pk_bytes):
#     pk = Ed25519PublicKey.from_public_bytes(pk_bytes)
#     return pk
#
#
# def bytes_to_sk(sk_bytes):
#     sk = Ed25519PrivateKey.from_private_bytes(sk_bytes)
#     return sk
#
#
# def pk_to_pem(pk):
#     pk_pem = pk.public_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PublicFormat.SubjectPublicKeyInfo
#     )
#     return pk_pem
#
#
# def sk_to_pem(sk):
#     sk_pem = sk.private_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PrivateFormat.PKCS8,
#         encryption_algorithm=serialization.NoEncryption()
#     )
#     return sk_pem
#
#
# def pem_to_pk(pk_pem):
#     if isinstance(pk_pem, str):
#         pk_pem = pk_pem.encode('utf-8')
#     pk = serialization.load_pem_public_key(pk_pem, backend=default_backend())
#     return pk
#
#
# def pem_to_sk(sk_pem):
#     if isinstance(sk_pem, str):
#         sk_pem = sk_pem.encode('utf-8')
#     sk = serialization.load_pem_private_key(sk_pem, None, backend=default_backend())
#     return sk
#
#
# def pem_to_pk_bytes(pk_pem):
#     pk = pem_to_pk(pk_pem)
#     pk_bytes = pk_to_bytes(pk)
#     return pk_bytes
#
#
# def pem_to_sk_bytes(sk_pem):
#     sk = pem_to_sk(sk_pem)
#     sk_bytes = sk_to_bytes(sk)
#     return sk_bytes
#
#
# def pk_bytes_to_pem(pk_bytes):
#     pk = bytes_to_pk(pk_bytes)
#     pk_pem = pk_to_pem(pk)
#     return pk_pem
#
#
# def sk_bytes_to_pem(sk_bytes):
#     sk = bytes_to_sk(sk_bytes)
#     sk_pem = sk_to_pem(sk)
#     return sk_pem
#
#
# # endregion


# 把字节串用base58编码格式编码
def bytes_to_base58(bytes_data: bytes):
    multikey = 'z' + base58.b58encode(bytes_data).decode()
    return multikey


# 把元组用base58格式编码
def tuple_to_base58(big_num_tuple: tuple):
    return bytes_to_base58(tuple_to_bytes(big_num_tuple))


# 生成did文档，公钥编码格式是base58
def gen_did_doc(did: str, pk_str: str):
    pk_bytes = to_bytes(pk_str)
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
            "publicKeyMultibase": bytes_to_base58(pk_bytes)
        }]
    }
    return json.dumps(did_doc, indent=4)


# 为一个csv文件添加一个新列
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
    gms_province_did = get_province_did('vcs/doc/gms_data.csv')
    print(gms_province_did)
    print(len(gms_province_did))

    # pk, sk = gen_key()
    # print('pk:', pk)
    # print('sk:', sk)
    #
    # pk_bytes = tuple_to_bytes(pk)
    # print('pk_bytes:', pk_bytes)
    #
    # pk_new = bytes_to_tuple(pk_bytes)
    # print('pk_new:', pk_new)
    #
    # sk_bytes = to_bytes(sk)
    # print('sk_bytes:', sk_bytes)
    #
    # sk_new = to_big_num(sk_bytes)
    # print('sk_new:', sk_new)

    # 示例数字
    # pk, sk = gen_key()
    # print('pk:', pk)
    # print('sk:', sk)
    #
    # print(gen_did('shanghai', pk))

    #
    # # 将数字转换为字节串，使用252位（ceil(252/8) = 32 字节）
    # # 计算所需字节长度
    # pk_x_byte = pk[0].to_bytes(byte_length, byteorder='big')
    # pk_y_byte = pk[1].to_bytes(byte_length, byteorder='big')
    # print('byte_length:', byte_length)
    # print('pk_x_byte:', pk_x_byte)
    # print('pk_y_byte:', pk_y_byte)
    #
    # # 将字节串转换回整数
    # decoded_x = int.from_bytes(pk_x_byte, byteorder='big')
    # decoded_y = int.from_bytes(pk_y_byte, byteorder='big')
    # print("decoded_x:", decoded_x)
    # print("decoded_y:", decoded_y)
