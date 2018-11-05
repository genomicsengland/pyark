import os
import pyark.cva_client as cva_client
from protocols.protocol_7_0.cva import Program, Assembly, ReportEventType
import logging
from enum import Enum
import collections


SIMILARITY_METRICS = ["RESNIK", "JACCARD", "PHENODIGM"]
REPORT_EVENT_TYPES = [ReportEventType.genomics_england_tiering, ReportEventType.candidate, ReportEventType.reported,
                      ReportEventType.questionnaire]


class CasesClient(cva_client.CvaClient):

    _BASE_ENDPOINT = "cases"

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def count(self, **params):
        return self.get_cases(count=True, **params)

    def get_cases(self, as_data_frame=False, **params):
        if params.get('count', False):
            results, next_page_params = self._get(self._BASE_ENDPOINT, params=params)
            return results[0]
        else:
            return self._paginate(endpoint=self._BASE_ENDPOINT, params=params, as_data_frame=as_data_frame)

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

    def get_summary(self, as_data_frame=False, params_list=[], **params):
        """
        :type as_data_frame: bool
        :type params_list: list
        :return:
        """
        if params_list:
            self._params_sanity_checks(params=params)
            results_list = [self.get_summary(params=p.update(params), as_data_frame=as_data_frame) for p in params_list]
            return self._render_multiple_results(results_list, as_data_frame=as_data_frame)
        else:
            results, _ = self._get("{endpoint}/summary".format(endpoint=self._BASE_ENDPOINT), params)
            if not results:
                logging.warning("No summary found")
                return None
            assert len(results) == 1, "Unexpected number of summaries"
            return self._render_single_result(results, as_data_frame=as_data_frame, indexes=params)

    @staticmethod
    def _params_sanity_checks(params):
        if not all(isinstance(p, dict) for p in params):
            raise ValueError("Cannot accept a list of 'params' not being only by dicts")
        keys = None
        for p in params:
            if keys is None:
                keys = set(p.keys())
            else:
                if len(set(p.keys()).difference(keys)) > 0:
                    raise ValueError("Cannot accept a list of 'params' with different lists of filters")

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
        return self._render(results, as_data_frame=as_data_frame)

    def get_case_by_identifiers(self, identifiers, as_data_frame=False):
        """
        :param as_data_frame: bool
        :type identifiers: list
        :return:
        """
        results, _ = self._get("{endpoint}/{identifiers}".format(
            endpoint=self._BASE_ENDPOINT, identifiers=",".join(identifiers)))
        return self._render(results, as_data_frame=as_data_frame)

    def search(self, query):
        results, _ = self._get("{endpoint}/search/{query}".format(endpoint=self._BASE_ENDPOINT, query=query))
        return self._render(results, as_data_frame=False)

    def get_variants_by_gene_id(self, program, assembly, gene_id,
                                include_aggregations=False, **params):
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
        return self._get(os.path.join(path), params)

    def get_variants_by_transcript_id(self, assembly, transcript_id, **params):
        """
        :type assembly: Assembly
        :type transcript_id: str
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                CasesClient._by_transcript_id(assembly, transcript_id),
                self._OutputEntities.variants.value]
        return self._get(os.path.join(path), params)

    def get_variants_by_gene_symbol(self, assembly, gene_symbol, **params):
        """
        :type assembly: Assembly
        :type gene_symbol: str
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                CasesClient._by_gene_symbol(assembly, gene_symbol),
                self._OutputEntities.variants.value]
        return self._get(os.path.join(path), params)

    def get_variants_by_panel(self, panel_name, **params):
        """
        :type panel_name: str
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                CasesClient._by_panel(panel_name),
                self._OutputEntities.variants.value]
        return self._get(os.path.join(path), params)

    def get_genes_by_panel(self, panel_name, **params):
        """
        :type panel_name: str
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                CasesClient._by_panel(panel_name),
                self._OutputEntities.genes.value]
        return self._get(os.path.join(path), params)

    def get_variants_by_genomic_region(self, assembly, chromosome, start, end, **params):
        """
        :type assembly: Assembly
        :type chromosome: str
        :type start: int
        :type end: int
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                CasesClient._by_genomic_coordinates(assembly, chromosome, start, end),
                self._OutputEntities.variants.value]
        return self._get(os.path.join(path), params)

    def get_phenotypes_by_gene_id(self, assembly, gene_id, **params):
        """
        :type assembly: Assembly
        :type gene_id: str
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                CasesClient._by_gene_id(assembly, gene_id),
                self._OutputEntities.phenotypes.value]
        return self._get(os.path.join(path), params)

    def get_phenotypes_by_transcript_id(self, assembly, transcript_id, **params):
        """
        :type assembly: Assembly
        :type transcript_id: str
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                CasesClient._by_transcript_id(assembly, transcript_id),
                self._OutputEntities.phenotypes.value]
        return self._get(os.path.join(path), params)

    def get_phenotypes_by_gene_symbol(self, assembly, gene_symbol, **params):
        """
        :type assembly: Assembly
        :type gene_symbol: str
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT, CasesClient._by_gene_symbol(assembly, gene_symbol),
                self._OutputEntities.phenotypes.value]
        return self._get(os.path.join(path), params)

    def get_phenotypes_by_genomic_region(self, assembly, chromosome, start, end, **params):
        """
        :type assembly: Assembly
        :type chromosome: str
        :type start: int
        :type end: int
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT, CasesClient._by_genomic_coordinates(assembly, chromosome, start, end),
                self._OutputEntities.phenotypes.value]
        return self._get(os.path.join(path), params)

    def get_genes_by_genomic_region(self, assembly, chromosome, start, end, **params):
        """
        :type assembly: Assembly
        :type chromosome: str
        :type start: int
        :type end: int
        :type params: dict
        :return:
        """
        path = [self._BASE_ENDPOINT,
                CasesClient._by_genomic_coordinates(assembly, chromosome, start, end),
                self._OutputEntities.genes.value]
        return self._get(os.path.join(path), params)

    def get_similar_cases_by_case(self, case_id, case_version, as_data_frame=False, **params):
        """
        :type as_data_frame: bool
        :type case_id: str
        :type case_version: int
        :type params: dict
        :return:
        """
        results, _ = self._get("{endpoint}/{case_id}/{case_version}/similar-cases".format(
            endpoint=self._BASE_ENDPOINT, case_id=case_id, case_version=case_version), params)
        if not results:
            logging.warning("No similar cases found")
            return None
        return self._render(results, as_data_frame=as_data_frame)

    def get_similar_cases_by_phenotypes(self, phenotypes, as_data_frame=False, **params):
        """
        :type as_data_frame: bool
        :type phenotypes: list
        :type params: dict
        :return:
        """
        params['hpoIds'] = phenotypes
        results, _ = self._get(
            "{endpoint}/phenotypes/similar-cases".format(endpoint=self._BASE_ENDPOINT), params)
        if not results:
            logging.warning("No similar cases found")
            return None
        return self._render(results, as_data_frame=as_data_frame)

    def get_shared_variants_cases_by_case(self, case_id, case_version, report_event_type, **params):
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
        params['type'] = report_event_type
        results, _ = self._get("{endpoint}/{case_id}/{case_version}/shared-variants".format(
            endpoint=self._BASE_ENDPOINT, case_id=case_id, case_version=case_version), params)
        if not results:
            logging.warning("No cases sharing {} variants found".format(report_event_type))
            return None
        return results

    def get_shared_genes_cases_by_case(self, case_id, case_version, report_event_type, **params):
        """
        :type case_id: str
        :type case_version: int
        :type report_event_type: ReportEventType
        :type params: dict
        :return:
        """
        assert report_event_type in REPORT_EVENT_TYPES, \
            "Invalid report event type provided '{}'. Valid values: {}".format(report_event_type, REPORT_EVENT_TYPES)
        if params is None:
            params = {}
        params['type'] = report_event_type
        results, _ = self._get("{endpoint}/{case_id}/{case_version}/shared-genes".format(
            endpoint=self._BASE_ENDPOINT, case_id=case_id, case_version=case_version), params)
        if not results:
            logging.warning("No cases sharing {} genes found".format(report_event_type))
            return None
        return results
