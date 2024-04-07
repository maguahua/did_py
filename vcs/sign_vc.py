import json
import time
from datetime import datetime

import base58
import pandas as pd

from src import User
from src.GM import GM
from src.ring import *
from utilities import get_province_did, tuple_to_bytes, str_to_tuple


# 把各个省份数据先存起来
def gen_gms_list():
    df = pd.read_csv('doc/gms_data.csv')
    gms_list = []
    for index, row in df.iterrows():
        sig_pk = str_to_tuple(row['sig_pk'])
        sig_sk = int(row['sig_sk'])
        aud_pk = str_to_tuple(row['aud_pk'])
        aud_sk = int(row['aud_sk'])
        gm = GM(row['province'], row['did'], sig_pk, sig_sk, row['did_doc'], aud_pk, aud_sk)
        gms_list.append(gm)
    return gms_list


# 从gm实例列表中中获取gm的省份和公钥，并形成一个字典{省份，GM签名公钥}
def get_dict_province_gmpks(gms_list) -> dict:
    province_gmpks = {gm.province: gm.sig_pk for gm in gms_list}
    return province_gmpks


# {省份，GM实例}
def get_dict_province_gm(gms_list) -> dict:
    province_gm = {}
    for gm in gms_list:
        province_gm[gm.province] = gm
    return province_gm


# 生成签名
def gen_sig(gms_pk_list, sig_key_pair: (tuple, int), vc_int):
    gms_pk_list, tees, cee = aosring_sign(gms_pk_list, sig_key_pair, None, None, vc_int)
    return gms_pk_list, tees, cee


# 生成proof字段
def gen_proof(gms_pk_list, province, sig_key, vc_int):
    gms_province_did = get_province_did('doc/gms_data.csv')
    # 签名的消息是整数形式
    signature = pks, tees, seed = gen_sig(gms_pk_list, sig_key, vc_int)
    proof = {
        "type": "Ed25519Signature2020",
        "created": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        "verificationMethod": gms_province_did[province],
        "proofPurpose": "assertionMethod",
        "proofValue": base58.b58encode(tuple_to_bytes(signature)).decode('utf-8')
    }
    return proof, signature


# 为某一个用户生成vc，为该vc签名的gm可以不是用户所在的省份
def gen_vc(gms_pk_list, gm: GM, user: User):
    signed_vc = json.loads(user.vc)
    signed_vc["@context"].append("https://w3id.org/security/suites/ed25519-2020/v1")

    vc_int = h1(user.vc.encode('utf-8'))
    proof, signature = gen_proof(gms_pk_list, gm.province, (gm.sig_pk, gm.sig_sk), vc_int)
    signed_vc["proof"] = proof
    # signed_vc["signature"] = signature

    user.signed_vc = json.dumps(signed_vc, indent=4)
    return signature


# 随机获取一个gm实例
# def get_rand_gm(gms_pk_dict: dict):
#     rand_gm = random.choice(gms_pk_dict)
#     return rand_gm


# 为所有用户生成vc
def sign_all_vc(users_data_filename):
    gms_list = gen_gms_list()  # 生成所有gm的实例并组成一个list
    # print("生成所有gm的实例并组成一个list")
    gms_pk_dict = get_dict_province_gmpks(gms_list)  # 方便查找，把省份和签名公钥构成一个字典
    dict_province_gm = get_dict_province_gm(gms_list)
    # print("为方便查找，把省份和签名公钥构成一个字典")
    # sig_gm = get_rand_gm(gms_pk_dict)
    gms_pk_list = list(gms_pk_dict.values())  # 把GM的签名密钥构成一个pkList
    # print("把GM的签名密钥构成一个pkList")

    # 在为所有用户生成vc的过程中，需要有签名gm的省份，sig_pk，被签名user的实例
    df = pd.read_csv(users_data_filename)
    df['signed_vc'] = None
    df['signature'] = None

    # 记录时间
    elapse_time_list = []

    for index, row in df.iterrows():
        # 开始时间
        start_time = time.time()

        pk = str_to_tuple(row['pk'])
        sk = int(row['sk'])
        user = User(row['province'], row['did'], pk, sk, row['did_doc'], row['vc'], None)
        sig_gm = dict_province_gm[user.province]
        signature = gen_vc(gms_pk_list, sig_gm, user)

        df.at[index, 'signed_vc'] = user.signed_vc
        df.at[index, 'signature'] = signature

        end_time = time.time()
        elapse_time = end_time - start_time
        df.at[index, 'elapse_time'] = elapse_time
        elapse_time_list.append(elapse_time)

        print(f"第{index}次执行了{elapse_time}秒")

    df.to_csv('doc/users_data.csv')


if __name__ == '__main__':
    sign_all_vc('doc/users_data.csv')
    print('done')
