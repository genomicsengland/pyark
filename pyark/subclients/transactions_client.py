from pyark import cva_client
from pyark.errors import CvaClientError
from protocols.protocol_7_0.cva import Transaction


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
        results = self._patch("{endpoint}/{identifier}".format(
            endpoint=self._BASE_ENDPOINT, identifier=transaction_id))

        def status_transform(x):
            return x[0]['response'][0]['result'][0]['status']

        self._format_results(results, status_transform, transaction_id, just_return_status)

    def count(self, **params):
        params['count'] = True
        return self.get_transactions(**params)

    def get_transactions(self, **params):
        if params.get('count', False):
            results, next_page_params = self._get(self._BASE_ENDPOINT, params=params)
            return results[0]
        else:
            return self._paginate_transactions(params)

    def _paginate_transactions(self, params):
        more_results = True
        while more_results:
            results, next_page_params = self._get(self._BASE_ENDPOINT, params=params)
            transactions = list(map(lambda x: Transaction.fromJsonDict(x), results))
            if next_page_params:
                params[cva_client.CvaClient._LIMIT_PARAM] = next_page_params[cva_client.CvaClient._LIMIT_PARAM]
                params[cva_client.CvaClient._MARKER_PARAM] = next_page_params[cva_client.CvaClient._MARKER_PARAM]
            else:
                more_results = False
            for transaction in transactions:
                yield transaction

    @staticmethod
    def _format_results(items, transform, transaction_id, just_return_status):
        try:
            if just_return_status:
                return transform(items)
            else:
                return items
        except (KeyError, IndexError):
            raise CvaClientError("no transaction for {}".format(transaction_id))
