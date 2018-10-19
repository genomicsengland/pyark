import pyark.cva_client as cva_client
import pandas as pd


class EntitiesClient(cva_client.CvaClient):

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def get_panels_summary(self, consider_versions=True, as_data_frame=False, latest=True):
        """
        :param latest: return only panels corresponding to latest cases
        :type latest: bool
        :param as_data_frame: return results in a flattened Pandas data frame or in a list of dictionaries
        :type as_data_frame: bool
        :param consider_versions: aggregates all versions of each panel or not
        :type consider_versions: bool
        :return: returns all observed panels and the number of cases on which they were applied.
        :rtype: list or pd.DataFrame
        """
        params = {'considerVersions': consider_versions, 'latest': latest}
        results, _ = self._get("panels/summary", params=params)
        return self._render(results, as_data_frame)

    def get_all_panels(self, latest=True):
        """
        :param latest: return only panels corresponding to latest cases
        :type latest: bool
        :return: return a list of observed panel names
        :rtype: pd.Series
        """
        results = self.get_panels_summary(consider_versions=False, latest=latest)
        all_panels = [x['panel']['panelName'] for x in results]
        return pd.Series(all_panels, index=all_panels)

    def get_disorders_summary(self, as_data_frame=False, latest=True):
        """
        :param latest: return only disorders corresponding to latest cases
        :type latest: bool
        :param as_data_frame: return results in a flattened Pandas data frame or in a list of dictionaries
        :type as_data_frame: bool
        :return:
        :rtype: list or pd.DataFrame
        """
        params = {'latest': latest}
        results, _ = self._get("disorders/summary", params=params)
        return self._render(results, as_data_frame)

    def get_all_specific_diseases(self, latest=True):
        """
        :param latest: return only disorders corresponding to latest cases
        :type latest: bool
        :return: return a list of observed specific diseases
        :rtype: pd.Series
        """
        results = self.get_disorders_summary(latest=latest)
        all_diseases = list(set([x['disorder']['specificDisease'] for x in results]))
        return pd.Series(all_diseases, index=all_diseases)

    def get_all_disease_groups(self, latest=True):
        """
        :param latest: return only disorders corresponding to latest cases
        :type latest: bool
        :return: return a list of observed disease groups
        :rtype: pd.Series
        """
        results = self.get_disorders_summary(latest=latest)
        all_disease_groups = list(set([x['disorder']['diseaseGroup'] for x in results]))
        return pd.Series(all_disease_groups, index=all_disease_groups)

    def get_all_disease_subgroups(self, latest=True):
        """
        :param latest: return only disorders corresponding to latest cases
        :type latest: bool
        :return: return a list of observed disease subgroups
        :rtype: pd.Series
        """
        results = self.get_disorders_summary(latest=latest)
        all_disease_subgroups = list(set([x['disorder']['diseaseSubGroup'] for x in results]))
        return pd.Series(all_disease_subgroups, index=all_disease_subgroups)
