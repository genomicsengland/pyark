from pyark import cva_client
from protocols.protocol_7_0.cva import EvidenceEntryAndVariants


class EvidencesClient(cva_client.CvaClient):

    _BASE_ENDPOINT = "evidences"

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def get_evidences(self, source, as_data_frame=False, **params):
        url = "{endpoint}/sources/{source}".format(endpoint=self._BASE_ENDPOINT, source=source)
        return self._paginate(endpoint=url, as_data_frame=as_data_frame, **params)

    def post_evidences(self, evidence, **params):
        """
        :type evidence: EvidenceEntryAndVariants
        :type params: dict
        :rtype: dict
        """
        return self._post(self._BASE_ENDPOINT, evidence.toJsonDict(), params)
