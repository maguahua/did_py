'''
本文件生成未签名VC
'''
from datetime import timedelta, datetime
from random import randint

from utilities import *


# 自己的did，自己的公钥，gm的did
def create_vc(did: str, pk_str: str, issuer: str):
    pk_bytes = to_bytes(pk_str)
    now = datetime.now()
    vc = {
        "@context": [
            "https://www.w3.org/ns/credentials/v2",
            "https://www.w3.org/ns/credentials/examples/v2"
        ],
        "id": f"http://grid.example/credentials/{randint(1000, 9999)}",
        "type": ["VerifiableCredential", "ExampleDegreeCredential"],
        "issuer": issuer,
        "validFrom": str(now.strftime("%Y-%m-%d %H:%M:%S")),
        "validUntil": str((now + timedelta(days=100)).strftime("%Y-%m-%d %H:%M:%S")),
        "credentialSubject": {
            "id": did,
            "type": [
                "GridIdentity",
                "User"
            ],
            "publicKey": bytes_to_base58(pk_bytes)
        },
    }
    return json.dumps(vc, indent=4)


def load_gm_dids(filename: str) -> dict:
    gms_did = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            province = row[0]
            did = row[1]
            gms_did[province] = did
    return gms_did


def gen_vcs(gms_data_filename, users_data_filename):
    # gm_dids[省份] = 省份did
    gms_did: dict = load_gm_dids(gms_data_filename)
    df = pd.read_csv(users_data_filename)
    df['vc'] = df.apply(lambda row: create_vc(row['did'], row['pk'], gms_did[row['province']]), axis=1)
    df.to_csv(users_data_filename, index=False)


if __name__ == '__main__':
    # 测试
    gen_vcs('doc/gms_data.csv', 'doc/users_data.csv')
    print('Done')
