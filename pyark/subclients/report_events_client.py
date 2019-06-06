from enum import Enum
from protocols.protocol_7_2.cva import ReportEventEntry, Assembly

import pyark.cva_client as cva_client
from pyark.models.wrappers import ReportEventEntryWrapper


class ReportEventsClient(cva_client.CvaClient):

    _BASE_ENDPOINT = "report-events"

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def count(self, **params):
        params['count'] = True
        return self.get_report_events(**params)

    def get_report_events(self, max_results=None, include_all=True, **params):
        """
        :type max_results: bool
        :type include_all: bool
        :type params: dict
        :rtype: int | ReportEventEntryWrapper
        """
        if params.get('count', False):
            results, next_page_params = self._get(self._BASE_ENDPOINT, **params)
            return results[0]
        else:
            if include_all:
                params['include'] = [self._INCLUDE_ALL]
            return self._paginate(
                endpoint=self._BASE_ENDPOINT, max_results=max_results,
                transformer=lambda x: ReportEventEntryWrapper.fromJsonDict(x), **params)

    def get_variant_summary_by_ids(self, variant_ids, **params):
        """
        :type variant_ids: list
        :rtyoe: list
        """
        if params is None:
            params = {}
        results, _ = self._post([self._BASE_ENDPOINT, "variant-summary-by-ids"], variant_ids, **params)
        return results

    def get_variant_summary_by_coordinates(self, variant_coordinates, **params):
        """
        :type variant_coordinates: list
        :rtyoe: list
        """
        if params is None:
            params = {}
        results, _ = self._post([self._BASE_ENDPOINT, "variant-summary-by-coordinates"], variant_coordinates, **params)
        return results
