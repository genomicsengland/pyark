from pyark import cva_client
from protocols.protocol_7_0.cva import EvidenceEntryAndVariants


class EvidencesClient(cva_client.CvaClient):

    _BASE_ENDPOINT = "evidences"

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def get_evidences(self, source, **params):
        url = "{endpoint}/sources/{source}".format(endpoint=self._BASE_ENDPOINT, source=source)
        results = self._paginate(endpoint=url, **params)
        return map(lambda x: EvidenceEntryAndVariants.fromJsonDict(x), results)

    def post_evidences(self, evidence, **params):
        """
        :type evidence: EvidenceEntryAndVariants
        :type params: dict
        :rtype: dict
        """
        return self._post(self._BASE_ENDPOINT, evidence.toJsonDict(), params)
