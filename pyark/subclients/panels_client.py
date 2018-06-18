import pyark.cva_client as cva_client


class PanelsClient(cva_client.CvaClient):

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def get_panels_summary(self, use_versions=True):
        """

        :type use_versions: bool
        :return:
        :rtype: list
        """
        params = {'use_versions': use_versions}
        results, _ = self.get("panels/summary", params=params)
        return results

    def get_all_panels(self):
        """
        :return:
        :rtype: list
        """
        results = self.get_panels_summary(use_versions=False)
        return [x['panel']['name'] for x in results]
