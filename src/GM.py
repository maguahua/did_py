class GM:
    def __init__(self, province, did, sig_pk, sig_sk, did_doc, aud_pk, aud_sk):
        self.province = province
        self.did = did
        self.did_doc = did_doc
        self.sig_pk = sig_pk
        self.sig_sk = sig_sk
        self.aud_pk = aud_pk
        self.aud_sk = aud_sk

