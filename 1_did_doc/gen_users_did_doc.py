import pandas as pd

from utilities import gen_did_doc, pem_to_pk_bytes


def gen_all_users_did_doc(users_file):
    df = pd.read_csv(users_file)
    df['did_doc'] = df.apply(lambda row: gen_did_doc(row['did'], pem_to_pk_bytes(row['pk'])), axis=1)
    df.to_csv(users_file, index=False)


if __name__ == '__main__':
    gen_all_users_did_doc('doc/users_data.csv')
    print('done')
