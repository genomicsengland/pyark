import pyark.cva_client as cva_client


class PanelsClient(cva_client.CvaClient):

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def get_panels_summary(self, program):
        """

        :param program:
        :type program: Program
        :return:
        :rtype: tuple
        """
        params = {'program': program}
        results, _ = self.get("panels/summary", params=params)
        return dict(map(lambda x: (frozenset(x['_id'].items()), {key: x[key] for key in x if key != '_id'}), results))

    def get_all_panels(self, include_versions=False, params={}):
        """

        :param include_versions:
        :param params:
        :return:
        :rtype: tuple
        """
        params['include_versions'] = include_versions
        results, _ = self.get("panels", params=params)
        return cva_client.CvaClient.results2list(results)