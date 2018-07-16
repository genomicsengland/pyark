from pyark import cva_client
from pyark.errors import CvaClientError


class TransactionsClient(cva_client.CvaClient):
    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def get_transaction(self, transaction_id, just_return_status=False):
        results = self.get("transactions/{identifier}".format(identifier=transaction_id))
        if just_return_status:
            return self._first_or_raise([r['status'] for s in results for r in s], transaction_id)
        else:
            return results

    def retry_transaction(self, transaction_id, just_return_status=False):
        results = self.patch("transactions/{identifier}".format(identifier=transaction_id))
        if just_return_status:
            return self._first_or_raise(
                [t['status'] for r in results for s in r['response'] for t in s['result']],
                transaction_id
            )
        return results

    def get_transactions(self, params={}):
        return self.get("transactions", params=params)

    @staticmethod
    def _first_or_raise(items, id):
        if items:
            return items[0]
        else:
            raise CvaClientError("no transaction for {}".format(id))
