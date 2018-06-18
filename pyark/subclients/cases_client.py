import pyark.cva_client as cva_client
from enum import Enum
from protocols.cva_1_0_0 import ReportEventEntry, Program, ReportEventType, Assembly
import logging


class CasesClient(cva_client.CvaClient):

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    class OutputEntities(Enum):
        variants = 'variants'
        phenotypes = 'phenotypes'
        genes = 'genes'

    @staticmethod
    def _by_program(program):
        return "cases/programs/{program}".format(program=program)

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

    def get_summary(self, params={}):
        """

        :type params: dict
        :return:
        """
        results, _ = self.get("cases/summary", params)
        if not results:
            logging.warning("No summary found")
            return None
        assert len(results) == 1, "Unexpected number of summaries"
        return results[0]

    def get_case(self, identifier, version):
        """

        :type identifier: str
        :type version: str
        :return:
        """
        results, _ = self.get("cases/{identifier}/{version}".format(identifier=identifier, version=version))
        if not results:
            logging.warning("No case found with id-version {}-{}".format(identifier, version))
            return None
        assert len(results) == 1, "Unexpected number of cases returned when searching by identifier"
        return results[0]

    def get_cases(self, params):
        """

        :param params:
        :return:
        """
        # TODO: implement!
        raise NotImplemented

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
        path = [CasesClient._by_program(program),
                CasesClient._by_gene_id(assembly, gene_id),
                self.OutputEntities.variants.value]
        return self.get_aggregation_query(path, include_aggregations, params)

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
        path = [CasesClient._by_program(program),
                CasesClient._by_transcript_id(assembly, transcript_id),
                self.OutputEntities.variants.value]
        return self.get_aggregation_query(path, include_aggregations, params)

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
        path = [CasesClient._by_program(program),
                CasesClient._by_gene_symbol(assembly, gene_symbol),
                self.OutputEntities.variants.value]
        return self.get_aggregation_query(path, include_aggregations, params)

    def get_variants_by_panel(self, panel_name, panel_version,
                              include_aggregations=False, params={}):
        """

        :type panel_name: str
        :type panel_version: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [CasesClient._by_panel(panel_name), self.OutputEntities.variants.value]
        if params is None:
            params = {}
        if panel_version:
            params['panel_version'] = panel_version
        return self.get_aggregation_query(path, include_aggregations, params)

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
        path = [CasesClient._by_program(program),
                CasesClient._by_genomic_coordinates(assembly, chromosome, start, end),
                self.OutputEntities.variants.value]
        return self.get_aggregation_query(path, include_aggregations, params)

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
        path = [CasesClient._by_program(program),
                CasesClient._by_gene_id(assembly, gene_id),
                self.OutputEntities.phenotypes.value]
        return self.get_aggregation_query(path, include_aggregations, params)

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
        path = [CasesClient._by_program(program),
                CasesClient._by_transcript_id(assembly, transcript_id),
                self.OutputEntities.phenotypes.value]
        return self.get_aggregation_query(path, include_aggregations, params)

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
        path = [CasesClient._by_program(program),
                CasesClient._by_gene_symbol(assembly, gene_symbol),
                self.OutputEntities.phenotypes.value]
        return self.get_aggregation_query(path, include_aggregations, params)

    def get_phenotypes_by_panel(self, panel_name, panel_version,
                                include_aggregations=False, params={}):
        """

        :type program: Program
        :type panel_name: str
        :type panel_version: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        # path = [CasesClient._by_panel(panel_name),
        #         self.OutputEntities.phenotypes.value]
        # if params is None:
        #     params = {}
        # if panel_version:
        #     params['panel_version'] = panel_version
        # return self.get_aggregation_query(path, include_aggregations, params)
        raise NotImplemented

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
        path = [CasesClient._by_program(program),
                CasesClient._by_genomic_coordinates(assembly, chromosome, start, end),
                self.OutputEntities.phenotypes.value]
        return self.get_aggregation_query(path, include_aggregations, params)

    def get_genes_by_panel(self, panel_name, panel_version,
                           include_aggregations=False, params={}):
        """

        :type panel_name: str
        :type panel_version: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        # path = [CasesClient._by_panel(panel_name),
        #         self.OutputEntities.genes.value]
        # if params is None:
        #     params = {}
        # if panel_version:
        #     params['panel_version'] = panel_version
        # return self.get_aggregation_query(path, include_aggregations, params)
        raise NotImplemented

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
        path = [CasesClient._by_program(program),
                CasesClient._by_genomic_coordinates(assembly, chromosome, start, end),
                self.OutputEntities.genes.value]
        return self.get_aggregation_query(path, include_aggregations, params)
