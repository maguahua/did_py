class User:
    def __init__(self, province, did, pk, sk, did_doc, vc, signed_vc=None, signature=None):
        self.province = province
        self.did = did
        self.pk = pk
        self.sk = sk
        self.did_doc = did_doc
        self.vc = vc
        self.signed_vc = signed_vc

        self.signature = signature
