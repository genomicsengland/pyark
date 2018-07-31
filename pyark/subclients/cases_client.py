import pyark.cva_client as cva_client
from protocols.cva_1_0_0 import Program, Assembly, ReportEventType
import logging
from enum import Enum

SIMILARITY_METRICS = ["RESNIK", "JACCARD", "PHENODIGM"]
REPORT_EVENT_TYPES = [ReportEventType.tiered, ReportEventType.candidate, ReportEventType.reported,
                      ReportEventType.questionnaire]


class CasesClient(cva_client.CvaClient):

    _BASE_ENDPOINT = "cases"

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def count_cases(self, params={}):
        if not params:
            params = {}
        params['count'] = True
        return self.get_cases(params)

    def get_cases(self, params={}):
        if params.get('count', False):
            results, next_page_params = self._get(self._BASE_ENDPOINT, params=params)
            return results[0]
        else:
            return self._paginate_cases(params)

    def _paginate_cases(self, params):
        more_results = True
        while more_results:
            results, next_page_params = self._get(self._BASE_ENDPOINT, params=params)
            cases = list(results)
            if next_page_params:
                params[cva_client.CvaClient._LIMIT_PARAM] = next_page_params[cva_client.CvaClient._LIMIT_PARAM]
                params[cva_client.CvaClient._MARKER_PARAM] = next_page_params[cva_client.CvaClient._MARKER_PARAM]
            else:
                more_results = False
            for case in cases:
                yield case

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
    def _by_panel(panel_name):
        return "panels/{panel_name}".format(panel_name=panel_name)

    @staticmethod
    def _by_genomic_coordinates(assembly, chromosome, start, end):
        return "genomic-regions/{assembly}/{chromosome}/{start}/{end}".format(
            assembly=assembly, chromosome=chromosome, start=start, end=end)

    def get_summary(self, params={}, as_data_frame=False):
        """
        :param as_data_frame: bool
        :type params: dict
        :return:
        """
        results, _ = self._get("{endpoint}/summary".format(endpoint=self._BASE_ENDPOINT), params)
        if not results:
            logging.warning("No summary found")
            return None
        assert len(results) == 1, "Unexpected number of summaries"
        return self._render_single_result(results, as_data_frame=as_data_frame)

    def get_case(self, identifier, version, as_data_frame=False):
        """
        :param as_data_frame: bool
        :type identifier: str
        :type version: str
        :return:
        """
        results, _ = self._get("{endpoint}/{identifier}/{version}".format(
            endpoint=self._BASE_ENDPOINT, identifier=identifier, version=version))
        if not results:
            logging.warning("No case found with id-version {}-{}".format(identifier, version))
            return None
        assert len(results) == 1, "Unexpected number of cases returned when searching by identifier"
        return self._render_single_result(results, as_data_frame=as_data_frame)

    def _get_cases_aggregation_query(self, path, program, include_aggregations, params):
        if params is None:
            params = {}
        if program:
            params['program'] = program
        return self._get_aggregation_query(path, include_aggregations, params)

    def get_variants_by_gene_id(self, program, assembly, gene_id,
                                include_aggregations=False, params={}):
        """
        :type program: Program
        :type assembly: Assembly
        :type gene_id: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                CasesClient._by_gene_id(assembly, gene_id),
                self._OutputEntities.variants.value]
        return self._get_cases_aggregation_query(path, program, include_aggregations, params)

    def get_variants_by_transcript_id(self, program, assembly, transcript_id,
                                      include_aggregations=False, params={}):
        """

        :type program: Program
        :type assembly: Assembly
        :type transcript_id: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                CasesClient._by_transcript_id(assembly, transcript_id),
                self._OutputEntities.variants.value]
        return self._get_cases_aggregation_query(path, program, include_aggregations, params)

    def get_variants_by_gene_symbol(self, program, assembly, gene_symbol,
                                    include_aggregations=False, params={}):
        """
        :type program: Program
        :type assembly: Assembly
        :type gene_symbol: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                CasesClient._by_gene_symbol(assembly, gene_symbol),
                self._OutputEntities.variants.value]
        return self._get_cases_aggregation_query(path, program, include_aggregations, params)

    def get_variants_by_panel(self, program, panel_name, panel_version,
                              include_aggregations=False, params={}):
        """
        :type program: Program
        :type panel_name: str
        :type panel_version: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                CasesClient._by_panel(panel_name),
                self._OutputEntities.variants.value]
        if params is None:
            params = {}
        if panel_version:
            params['panel_version'] = panel_version
        return self._get_cases_aggregation_query(path, program, include_aggregations, params)

    def get_genes_by_panel(self, program, panel_name, panel_version,
                              include_aggregations=False, params={}):
        """
        :type program: Program
        :type panel_name: str
        :type panel_version: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                CasesClient._by_panel(panel_name),
                self._OutputEntities.genes.value]
        if params is None:
            params = {}
        if panel_version:
            params['panel_version'] = panel_version
        return self._get_cases_aggregation_query(path, program, include_aggregations, params)

    def get_variants_by_genomic_region(self, program, assembly, chromosome, start, end,
                                       include_aggregations=False, params={}):
        """

        :type program: Program
        :type assembly: Assembly
        :type chromosome: str
        :type start: int
        :type end: int
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                CasesClient._by_genomic_coordinates(assembly, chromosome, start, end),
                self._OutputEntities.variants.value]
        return self._get_cases_aggregation_query(path, program, include_aggregations, params)

    def get_phenotypes_by_gene_id(self, program, assembly, gene_id,
                                  include_aggregations=False, params={}):
        """

        :type program: Program
        :type assembly: Assembly
        :type gene_id: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                CasesClient._by_gene_id(assembly, gene_id),
                self._OutputEntities.phenotypes.value]
        return self._get_cases_aggregation_query(path, program, include_aggregations, params)

    def get_phenotypes_by_transcript_id(self, program, assembly, transcript_id,
                                        include_aggregations=False, params={}):
        """

        :type program: Program
        :type assembly: Assembly
        :type transcript_id: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                CasesClient._by_transcript_id(assembly, transcript_id),
                self._OutputEntities.phenotypes.value]
        return self._get_cases_aggregation_query(path, program, include_aggregations, params)

    def get_phenotypes_by_gene_symbol(self, program, assembly, gene_symbol,
                                      include_aggregations=False, params={}):
        """

        :type program: Program
        :type assembly: Assembly
        :type gene_symbol: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                CasesClient._by_gene_symbol(assembly, gene_symbol),
                self._OutputEntities.phenotypes.value]
        return self._get_cases_aggregation_query(path, program, include_aggregations, params)

    def get_phenotypes_by_genomic_region(self, program, assembly, chromosome, start, end,
                                         include_aggregations=False, params={}):
        """

        :type program: Program
        :type assembly: Assembly
        :type chromosome: str
        :type start: int
        :type end: int
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                CasesClient._by_genomic_coordinates(assembly, chromosome, start, end),
                self._OutputEntities.phenotypes.value]
        return self._get_cases_aggregation_query(path, program, include_aggregations, params)

    def get_genes_by_genomic_region(self, program, assembly, chromosome, start, end,
                                    include_aggregations=False, params={}):
        """

        :type program: Program
        :type assembly: Assembly
        :type chromosome: str
        :type start: int
        :type end: int
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                CasesClient._by_genomic_coordinates(assembly, chromosome, start, end),
                self._OutputEntities.genes.value]
        return self._get_cases_aggregation_query(path, program, include_aggregations, params)

    def get_similar_cases_by_case(self, case_id, case_version, similarity_metric, limit=50, params={}):
        """
        :type case_id: str
        :type case_version: int
        :type similarity_metric: str
        :type limit: int
        :type params: dict
        :return:
        """
        assert similarity_metric in SIMILARITY_METRICS, \
            "Invalid similarity metric provided '{}'. Valid values: {}".format(similarity_metric, SIMILARITY_METRICS)

        if params is None:
            params = {}
        params['similarity_metric'] = similarity_metric
        params['limit'] = limit
        results, _ = self._get("{endpoint}/{case_id}/{case_version}/similar-cases".format(
            endpoint=self._BASE_ENDPOINT, case_id=case_id, case_version=case_version), params)
        if not results:
            logging.warning("No similar cases found")
            return None
        return results

    def get_similar_cases_by_phenotypes(self, phenotypes, similarity_metric, limit=50, params={}):
        """
        :type phenotypes: list
        :type similarity_metric: str
        :type limit: int
        :type params: dict
        :return:
        """
        assert similarity_metric in SIMILARITY_METRICS, \
            "Invalid similarty metric provided '{}'. Valid values: {}".format(similarity_metric, SIMILARITY_METRICS)
        assert len(phenotypes) > 0, "At least one phenotype must be provided"
        if params is None:
            params = {}
        params['similarity_metric'] = similarity_metric
        params['limit'] = limit
        params['hpo_ids'] = phenotypes
        results, _ = self._get(
            "{endpoint}/phenotypes/similar-cases".format(endpoint=self._BASE_ENDPOINT), params)
        if not results:
            logging.warning("No similar cases found")
            return None
        return results

    def get_shared_variants_cases_by_case(self, case_id, case_version, report_event_type, limit=10, params={}):
        """
        :type case_id: str
        :type case_version: int
        :type report_event_type: ReportEventType
        :type limit: int
        :type params: dict
        :return:
        """
        assert report_event_type in REPORT_EVENT_TYPES, \
            "Invalid report event type provided '{}'. Valid values: {}".format(report_event_type, REPORT_EVENT_TYPES)
        if params is None:
            params = {}
        params['type'] = report_event_type
        params['limit'] = limit
        results, _ = self._get("{endpoint}/{case_id}/{case_version}/shared-variants".format(
            endpoint=self._BASE_ENDPOINT, case_id=case_id, case_version=case_version), params)
        if not results:
            logging.warning("No cases sharing {} variants  found".format(report_event_type))
            return None
        return results
