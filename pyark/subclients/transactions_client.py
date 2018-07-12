from pyark import cva_client


class TransactionsClient(cva_client.CvaClient):
    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def get_transaction(self, transaction_id):
        return self.get("transactions/{identifier}".format(identifier=transaction_id))

    def retry_transaction(self, transaction_id):
        return self.patch("transactions/{identifier}".format(identifier=transaction_id))

    def get_transactions(self, params={}):
        return self.get("transactions", params=params)
