import pyark.cva_client as cva_client
from enum import Enum
from protocols.cva_1_0_0 import ReportEventEntry, Program, ReportEventType, Assembly


class ReportEventsClient(cva_client.CvaClient):

    _BASE_ENDPOINT = "report-events"

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def count_report_events(self, params={}):
        if not params:
            params = {}
        params['count'] = True
        return self.get_report_events(params)

    def get_report_events(self, params={}):
        if params.get('count', False):
            results, next_page_params = self._get(self._BASE_ENDPOINT, params=params)
            return results[0]
        else:
            return self._paginate_report_events(params)

    def _paginate_report_events(self, params):
        more_results = True
        while more_results:
            results, next_page_params = self._get(self._BASE_ENDPOINT, params=params)
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
        phenotypes = 'phenotypes'
        genes = 'genes'

    @staticmethod
    def _by_gene_id(assembly, gene_id):
        return "gene-ids/{assembly}/{gene_id}".format(assembly=assembly, gene_id=gene_id)

    @staticmethod
    def _by_transcript_id(assembly, transcript_id):
        return "transcript-ids/{assembly}/{transcript_id}".format(assembly=assembly, transcript_id=transcript_id)

    @staticmethod
    def _by_gene_symbol(assembly, gene_symbol):
        return "gene-symbols/{assembly}/{gene_symbol}".format(assembly=assembly, gene_symbol=gene_symbol)

    @staticmethod
    def _by_genomic_coordinates(assembly, chromosome, start, end):
        return "genomic-regions/{assembly}/{chromosome}/{start}/{end}".format(
            assembly=assembly, chromosome=chromosome, start=start, end=end)

    def _get_report_events_aggregation_query(self, path, program, report_event_type, include_aggregations, params):
        if params is None:
            params = {}
        if program:
            params['program'] = program
        if report_event_type:
            params['type'] = report_event_type
        return self._get_aggregation_query(path, include_aggregations, params)

    def get_variants_by_gene_id(self, program, report_event_type, assembly, gene_id,
                                include_aggregations=False, params={}):
        """

        :type program: Program
        :type report_event_type: ReportEventType
        :type assembly: Assembly
        :type gene_id: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                ReportEventsClient._by_gene_id(assembly, gene_id),
                self._OutputEntities.variants.value]
        return self._get_report_events_aggregation_query(
            path, program, report_event_type, include_aggregations, params)

    def get_variants_by_transcript_id(self, program, report_event_type, assembly, transcript_id,
                                      include_aggregations=False, params={}):
        """

        :type program: Program
        :type report_event_type: ReportEventType
        :type assembly: Assembly
        :type transcript_id: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                ReportEventsClient._by_transcript_id(assembly, transcript_id),
                self._OutputEntities.variants.value]
        return self._get_report_events_aggregation_query(
            path, program, report_event_type, include_aggregations, params)

    def get_variants_by_gene_symbol(self, program, report_event_type, assembly, gene_symbol,
                                    include_aggregations=False, params={}):
        """

        :type program: Program
        :type report_event_type: ReportEventType
        :type assembly: Assembly
        :type gene_symbol: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                ReportEventsClient._by_gene_symbol(assembly, gene_symbol),
                self._OutputEntities.variants.value]
        return self._get_report_events_aggregation_query(
            path, program, report_event_type, include_aggregations, params)

    def get_variants_by_genomic_region(self, program, report_event_type, assembly, chromosome, start, end,
                                       include_aggregations=False, params={}):
        """

        :type program: Program
        :type report_event_type: ReportEventType
        :type assembly: Assembly
        :type chromosome: str
        :type start: int
        :type end: int
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                ReportEventsClient._by_genomic_coordinates(assembly, chromosome, start, end),
                self._OutputEntities.variants.value]
        return self._get_report_events_aggregation_query(
            path, program, report_event_type, include_aggregations, params)

    def get_phenotypes_by_gene_id(self, program, report_event_type, assembly, gene_id,
                                  include_aggregations=False, params={}):
        """

        :type program: Program
        :type report_event_type: ReportEventType
        :type assembly: Assembly
        :type gene_id: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                ReportEventsClient._by_gene_id(assembly, gene_id),
                self._OutputEntities.phenotypes.value]
        return self._get_report_events_aggregation_query(
            path, program, report_event_type, include_aggregations, params)

    def get_phenotypes_by_transcript_id(self, program, report_event_type, assembly, transcript_id,
                                        include_aggregations=False, params={}):
        """

        :type program: Program
        :type report_event_type: ReportEventType
        :type assembly: Assembly
        :type transcript_id: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                ReportEventsClient._by_transcript_id(assembly, transcript_id),
                self._OutputEntities.phenotypes.value]
        return self._get_report_events_aggregation_query(
            path, program, report_event_type, include_aggregations, params)

    def get_phenotypes_by_gene_symbol(self, program, report_event_type, assembly, gene_symbol,
                                      include_aggregations=False, params={}):
        """

        :type program: Program
        :type report_event_type: ReportEventType
        :type assembly: Assembly
        :type gene_symbol: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                ReportEventsClient._by_gene_symbol(assembly, gene_symbol),
                self._OutputEntities.phenotypes.value]
        return self._get_report_events_aggregation_query(
            path, program, report_event_type, include_aggregations, params)

    def get_phenotypes_by_genomic_region(self, program, report_event_type, assembly, chromosome, start, end,
                                         include_aggregations=False, params={}):
        """

        :type program: Program
        :type report_event_type: ReportEventType
        :type assembly: Assembly
        :type chromosome: str
        :type start: int
        :type end: int
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                ReportEventsClient._by_genomic_coordinates(assembly, chromosome, start, end),
                self._OutputEntities.phenotypes.value]
        return self._get_report_events_aggregation_query(
            path, program, report_event_type, include_aggregations, params)

    def get_genes_by_genomic_region(self, program, report_event_type, assembly, chromosome, start, end,
                                    include_aggregations=False, params={}):
        """

        :type program: Program
        :type report_event_type: ReportEventType
        :type assembly: Assembly
        :type chromosome: str
        :type start: int
        :type end: int
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                ReportEventsClient._by_genomic_coordinates(assembly, chromosome, start, end),
                self._OutputEntities.genes.value]
        return self._get_report_events_aggregation_query(
            path, program, report_event_type, include_aggregations, params)
