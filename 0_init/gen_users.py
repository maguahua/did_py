'''
随机生成1000个用户，did、did_doc、pk、sk、vc

did共三个部分
Scheme : Did Method : DID Method-Specific Identifier
在本次实验中，用户的did，公钥，私钥都存储在一个文件中，这在现实中是不可取的
'''

import csv
import random

from utilities import gen_provinces, gen_key_pair, gen_did, pk_to_pem, sk_to_pem


def gen_all_users_did(users_file, users_num):
    provinces_tuple = gen_provinces('doc/province.csv')
    with open(users_file, 'w', newline='') as f:
        fieldnames = ['province', 'did', 'pk', 'sk']
        writer = csv.writer(f)

        # 写入表头
        writer.writerow(fieldnames)

        for _ in range(users_num):
            pk, sk = gen_key_pair()
            province = random.choice(provinces_tuple)
            did = gen_did(province, pk)
            row = [province, did, pk_to_pem(pk).decode(), sk_to_pem(sk).decode()]

            writer.writerow(row)


if __name__ == '__main__':
    # 生成 CSV 文件，例如生成10行数据
    gen_all_users_did('doc/users_data.csv', 1000)
