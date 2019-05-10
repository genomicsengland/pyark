from pyark import cva_client
from protocols.protocol_7_2.cva import Transaction


class TransactionsClient(cva_client.CvaClient):

    _BASE_ENDPOINT = "transactions"

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def get_transaction(self, transaction_id):
        """
        :type transaction_id: str
        :rtype: Transaction
        """
        results, _ = self._get("{endpoint}/{identifier}".format(
            endpoint=self._BASE_ENDPOINT, identifier=transaction_id))
        result = self._render_single_result(results, as_data_frame=False)
        return Transaction.fromJsonDict(result) if result else None

    def retry_transaction(self, transaction_id):
        """
        :type transaction_id: str
        :rtype: Transaction
        """
        results, _ = self._patch("{endpoint}/{identifier}".format(
            endpoint=self._BASE_ENDPOINT, identifier=transaction_id))
        result = self._render_single_result(results, as_data_frame=False)
        return Transaction.fromJsonDict(result) if result else None

    def count(self, **params):
        params['count'] = True
        return self.get_transactions(**params)

    def get_transactions(self, **params):
        """
        :param params:
        :rtype: Transaction or int
        """
        if params.get('count', False):
            results, next_page_params = self._get(self._BASE_ENDPOINT, **params)
            return results[0]
        else:
            return self._paginate_transactions(**params)

    def _paginate_transactions(self, **params):
        more_results = True
        while more_results:
            results, next_page_params = self._get(self._BASE_ENDPOINT, **params)
            transactions = list(map(lambda x: Transaction.fromJsonDict(x), results))
            if next_page_params:
                params[cva_client.CvaClient._LIMIT_PARAM] = next_page_params[cva_client.CvaClient._LIMIT_PARAM]
                params[cva_client.CvaClient._MARKER_PARAM] = next_page_params[cva_client.CvaClient._MARKER_PARAM]
            else:
                more_results = False
            for transaction in transactions:
                yield transaction
