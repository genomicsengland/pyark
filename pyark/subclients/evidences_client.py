from pyark import cva_client


class EvidencesClient(cva_client.CvaClient):

    _BASE_ENDPOINT = "evidences"

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def get_evidences(self, source, as_data_frame=False, **params):
        url = "{endpoint}/{source}".format(endpoint=self._BASE_ENDPOINT, source=source)
        return self._paginate(endpoint=url, as_data_frame=as_data_frame, **params)
