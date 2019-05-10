from enum import Enum
from protocols.protocol_7_2.cva import ReportEventEntry, Assembly

import pyark.cva_client as cva_client


class ReportEventsClient(cva_client.CvaClient):

    _BASE_ENDPOINT = "report-events"

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def count(self, **params):
        params['count'] = True
        return self.get_report_events(**params)

    def get_report_events(self, **params):
        if params.get('count', False):
            results, next_page_params = self._get(self._BASE_ENDPOINT, **params)
            return results[0]
        else:
            return self._paginate_report_events(**params)

    def _paginate_report_events(self, **params):
        more_results = True
        while more_results:
            results, next_page_params = self._get(self._BASE_ENDPOINT, **params)
            report_events = list(map(lambda x: ReportEventEntry.fromJsonDict(x), results))
            if next_page_params:
                params[cva_client.CvaClient._LIMIT_PARAM] = next_page_params[cva_client.CvaClient._LIMIT_PARAM]
                params[cva_client.CvaClient._MARKER_PARAM] = next_page_params[cva_client.CvaClient._MARKER_PARAM]
            else:
                more_results = False
            for report_event in report_events:
                yield report_event

    class _OutputEntities(Enum):
        variants = 'variants'
        genes = 'genes'

    @staticmethod
    def _by_gene_id(assembly, gene_id):
        return ["genes", assembly, gene_id]

    @staticmethod
    def _by_transcript_id(assembly, transcript_id):
        return ["transcripts", assembly, transcript_id]

    @staticmethod
    def _by_genomic_coordinates(assembly, chromosome, start, end):
        return ["genomic-regions", assembly, chromosome, start, end]

    def get_variants_by_gene_id(self, assembly, gene_id, **params):
        """
        :type assembly: Assembly
        :type gene_id: str
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT] + ReportEventsClient._by_gene_id(assembly, gene_id) + \
               [self._OutputEntities.variants.value]
        results, _ = self._get(path, **params)
        return results

    def get_variants_by_transcript_id(self, assembly, transcript_id, **params):
        """
        :type assembly: Assembly
        :type transcript_id: str
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT] + ReportEventsClient._by_transcript_id(assembly, transcript_id) + \
               [self._OutputEntities.variants.value]
        results, _ = self._get(path, **params)
        return results

    def get_variants_by_genomic_region(self, assembly, chromosome, start, end, **params):
        """
        :type assembly: Assembly
        :type chromosome: str
        :type start: int
        :type end: int
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT] + ReportEventsClient._by_genomic_coordinates(assembly, chromosome, start, end) + \
               [self._OutputEntities.variants.value]
        results, _ = self._get(path, **params)
        return results

    def get_genes_by_genomic_region(self, assembly, chromosome, start, end, **params):
        """
        :type assembly: Assembly
        :type chromosome: str
        :type start: int
        :type end: int
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT] + ReportEventsClient._by_genomic_coordinates(assembly, chromosome, start, end) + \
               [self._OutputEntities.genes.value]
        results, _ = self._get(path, **params)
        return results
