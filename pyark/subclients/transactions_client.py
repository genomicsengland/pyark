from pyark import cva_client


class TransactionsClient(cva_client.CvaClient):
    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def get_transaction(self, transaction_id, just_return_status=False):
        result = self.get("transactions/{identifier}".format(identifier=transaction_id))
        if just_return_status:
            return result[0][0]['status']
        return result

    def retry_transaction(self, transaction_id, just_return_status=False):
        result = self.patch("transactions/{identifier}".format(identifier=transaction_id))
        if just_return_status:
            return result[0]['response'][0]['result'][0]['status']
        return result

    def get_transactions(self, params={}):
        return self.get("transactions", params=params)
