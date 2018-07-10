from pyark import cva_client


class DataInjestClient(cva_client.CvaClient):
    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def post_pedigree(self, pedigree, params={}):
        return self.post(self.PEDIGREE_POST, pedigree.toJsonDict(), params)

    def post_participant(self, participant, params={}):
        return self.post(self.PARTICIPANT_POST, participant.toJsonDict(), params)
