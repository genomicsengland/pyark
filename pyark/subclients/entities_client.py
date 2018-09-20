import pyark.cva_client as cva_client


class EntitiesClient(cva_client.CvaClient):

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def get_panels_summary(self, use_versions=True, as_data_frame=False):
        """
        :param as_data_frame: bool
        :type use_versions: bool
        :return:
        :rtype: list
        """
        params = {'use_versions': use_versions}
        results, _ = self._get("panels/summary", params=params)
        return self._render(results, as_data_frame)

    def get_all_panels(self):
        """
        :return:
        :rtype: list
        """
        results = self.get_panels_summary(use_versions=False)
        return [x['panel']['name'] for x in results]

    def get_disorders_summary(self, as_data_frame=False):
        """
        :param as_data_frame: bool
        :return:
        :rtype: list
        """
        results, _ = self._get("disorders/summary")
        return self._render(results, as_data_frame)

    def get_all_specific_diseases(self):
        """
        :return:
        :rtype: list
        """
        results = self.get_disorders_summary()
        return [x['disorder']['specificDisease'] for x in results]

    def get_all_disease_groups(self):
        """
        :return:
        :rtype: list
        """
        results = self.get_disorders_summary()
        return [x['disorder']['diseaseGroup'] for x in results]

    def get_all_disease_subgroups(self):
        """
        :return:
        :rtype: list
        """
        results = self.get_disorders_summary()
        return [x['disorder']['diseaseSubGroup'] for x in results]
