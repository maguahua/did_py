'''
根据省份csv文件生成省份、did、did_doc、sig_pk、sig_sk、aud_pk、aud_sk
'''

import csv

from utilities import gen_provinces, gen_key_pair, gen_did, pk_to_pem, sk_to_pem


def gen_all_gms(gms_file):
    provinces_tuple = gen_provinces('doc/province.csv')
    with open(gms_file, 'w', newline='') as f:
        fieldnames = ['province', 'did', 'sig_pk', 'sig_sk']
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        for province in provinces_tuple:
            sig_pk, sig_sk = gen_key_pair()

            did = gen_did(province, sig_pk)
            row = [province, did, pk_to_pem(sig_pk).decode(), sk_to_pem(sig_sk).decode()]
            writer.writerow(row)


if __name__ == '__main__':
    gen_all_gms('doc/gms_data.csv')
