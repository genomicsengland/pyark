from pyark import cva_client


class DataInjestClient(cva_client.CvaClient):
    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def post_pedigree(self, pedigree, params={}):
        return self.post(self.PEDIGREE_POST, pedigree.toJsonDict(), params)

    def post_participant(self, participant, params={}):
        return self.post(self.PARTICIPANT_POST, participant.toJsonDict(), params)

    def post_tiered_variant(self, tiered_variant, params={}):
        return self.post(self.TIERED_VARIANT_RD_POST, tiered_variant.toJsonDict(), params)

    def post_candidate_variant(self, candidate_variant, params={}):
        return self.post(self.CANDIDATE_VARIANT_RD_POST, candidate_variant.toJsonDict(), params)

    def post_reported_variant(self, reported_variant, params={}):
        return self.post(self.REPORTED_VARIANT_RD_POST, reported_variant.toJsonDict(), params)

    def post_tiered_variant_cancer(self, tiered_variant, params={}):
        return self.post(self.TIERED_VARIANT_CANCER_POST, tiered_variant.toJsonDict(), params)

    def post_candidate_variant_cancer(self, candidate_variant, params={}):
        return self.post(self.CANDIDATE_VARIANT_CANCER_POST, candidate_variant.toJsonDict(), params)

    def post_reported_variant_cancer(self, reported_variant, params={}):
        return self.post(self.REPORTED_VARIANT_CANCER_POST, reported_variant.toJsonDict(), params)
