import time

import pandas as pd

from src import User
from src.ring import h1, aosring_check
from utilities import str_to_tuple, str_sig_to_tuple


def get_data():
    df_users = pd.read_csv('doc/users_data.csv')
    users_list = []

    for index, row in df_users.iterrows():
        pk = str_to_tuple(row['pk'])
        sk = int(row['sk'])
        signature = str_sig_to_tuple(row['signature'])
        user = User(row['province'], row['did'], pk, sk, row['did_doc'], row['vc'], row['signed_vc'], signature)

        users_list.append(user)

    return users_list


def check_vc(user):
    vc = user.vc
    signature = user.signature
    vc_int = h1(vc.encode('utf-8'))
    return aosring_check(*signature, vc_int)


if __name__ == "__main__":

    users_list = get_data()
    # user1 = random.choice(users_list)
    # user2 = random.choice(users_list)
    #
    # vc = user1.vc
    # signature = user2.signature
    # print(aosring_check(*signature,h1(vc.encode('utf-8'))))

    elapse_time_list = []

    for i in range(len(users_list)):
        start_time = time.time()

        print(i, check_vc(users_list[i]))

        end_time = time.time()
        elapse_time = end_time - start_time
        elapse_time_list.append(elapse_time)

    df = pd.DataFrame()
    df['elapse_time'] = elapse_time_list
    df.to_csv('doc/VC validation time.csv')
