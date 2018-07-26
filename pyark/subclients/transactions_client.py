from pyark import cva_client
from pyark.errors import CvaClientError


class TransactionsClient(cva_client.CvaClient):

    _BASE_ENDPOINT = "transactions"

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def get_transaction(self, transaction_id, just_return_status=False):
        results = self._get("{endpoint}/{identifier}".format(
            endpoint=self._BASE_ENDPOINT, identifier=transaction_id))

        def status_transform(x):
            return x[0][0]['status']

        return self._format_results(results, status_transform, transaction_id, just_return_status)

    def retry_transaction(self, transaction_id, just_return_status=False):
        results = self.patch("{endpoint}/{identifier}".format(
            endpoint=self._BASE_ENDPOINT, identifier=transaction_id))

        def status_transform(x):
            return x[0]['response'][0]['result'][0]['status']

        self._format_results(results, status_transform, transaction_id, just_return_status)

    def get_transactions(self, params={}):
        return self._get(self._BASE_ENDPOINT, params=params)

    @staticmethod
    def _format_results(items, transform, transaction_id, just_return_status):
        try:
            if just_return_status:
                return transform(items)
            else:
                return items
        except (KeyError, IndexError):
            raise CvaClientError("no transaction for {}".format(transaction_id))
