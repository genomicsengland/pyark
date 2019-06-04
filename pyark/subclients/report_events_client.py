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

    def get_report_events(self, **params):
        """
        :param params:
        :rtype: int | ReportEventEntryWrapper
        """
        if params.get('count', False):
            results, next_page_params = self._get(self._BASE_ENDPOINT, **params)
            return results[0]
        else:
            return self._paginate_report_events(**params)

    def _paginate_report_events(self, **params):
        more_results = True
        while more_results:
            results, next_page_params = self._get(self._BASE_ENDPOINT, **params)
            report_events = list(map(lambda x: ReportEventEntryWrapper.fromJsonDict(x), results))
            if next_page_params:
                params[cva_client.CvaClient._LIMIT_PARAM] = next_page_params[cva_client.CvaClient._LIMIT_PARAM]
                params[cva_client.CvaClient._MARKER_PARAM] = next_page_params[cva_client.CvaClient._MARKER_PARAM]
            else:
                more_results = False
            for report_event in report_events:
                yield report_event
