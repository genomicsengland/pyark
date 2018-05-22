import os
import logging
from unittest import TestCase
from protocols.reports_5_0_0 import Program
from protocols.cva_1_0_0 import ReportEventType, Assembly, Variant

from pyark.cva_client import CvaClient


class TestPyArk (TestCase):
    # credentials
    CVA_URL_BASE = os.getenv("CVA_URL")
    GEL_USER = os.getenv("GEL_USER")
    GEL_PASSWORD = os.getenv("GEL_PASSWORD")

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        if self.GEL_PASSWORD is None:
            self.GEL_PASSWORD = ""
        if not self.CVA_URL_BASE or not self.GEL_USER:
            logging.error("Please set the configuration environment variables: CVA_URL, GEL_USER, GEL_PASSWORD")
            raise ValueError("Missing config")
        self.cva = CvaClient(self.CVA_URL_BASE, user=self.GEL_USER, password=self.GEL_PASSWORD)
        self.report_events = self.cva.report_events()
        self.panels = self.cva.panels()
        self.cases = self.cva.cases()
        self.variants = self.cva.variants()

    def test_get_report_events(self):

        # all_report_events = self.report_events.get_report_events()
        # page_count = 0
        # for batch_report_events in all_report_events:
        #     self.assertTrue(batch_report_events is not None)
        #     # self.assertEqual(len(batch_report_events), 200)
        #     # logging.info("Returned {} report events".format(len(batch_report_events)))
        #     page_count += 1
        #     if page_count == 5:
        #         break
        # self.assertEqual(page_count, 5)

        all_report_events = self.report_events.get_report_events({'limit': 10})
        page_count = 0
        for batch_report_events in all_report_events:
            self.assertTrue(batch_report_events is not None)
            # self.assertEqual(len(batch_report_events), 10)
            # logging.info("Returned {} report events".format(len(batch_report_events)))
            page_count += 1
            if page_count == 5:
                break
        self.assertEqual(page_count, 5)

    def test_get_by_gene_id(self):

        gene_id = "ENSG00000130826"

        # gets variants
        results = self.report_events.get_variants_by_gene_id(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            gene_id, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_variants_by_gene_id(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            gene_id, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets phenotypes
        results = self.report_events.get_phenotypes_by_gene_id(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            gene_id, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_phenotypes_by_gene_id(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            gene_id, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

    def test_get_variants_by_transcript_id(self):

        tx_id = "ENST00000426673"

        # gets variants
        results = self.report_events.get_variants_by_transcript_id(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            tx_id, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_variants_by_transcript_id(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            tx_id, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets phenotypes
        results = self.report_events.get_phenotypes_by_transcript_id(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            tx_id, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_phenotypes_by_transcript_id(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            tx_id, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

    def test_get_variants_by_gene_symbol(self):

        gene_symbol = "BRCA1"

        # gets variants
        results = self.report_events.get_variants_by_gene_symbol(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            gene_symbol, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_variants_by_gene_symbol(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            gene_symbol, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets phenotypes
        results = self.report_events.get_phenotypes_by_gene_symbol(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            gene_symbol, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_phenotypes_by_gene_symbol(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            gene_symbol, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

    def test_get_variants_by_panel(self):

        panel_name = "cakut"

        # gets variants
        results = self.report_events.get_variants_by_panel(
            ReportEventType.tiered, panel_name, None, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_variants_by_panel(
            ReportEventType.tiered, panel_name, None, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets phenotypes
        results = self.report_events.get_phenotypes_by_panel(
            ReportEventType.tiered, panel_name, None, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_phenotypes_by_panel(
            ReportEventType.tiered, panel_name, None, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets genes
        results = self.report_events.get_genes_by_panel(
            ReportEventType.tiered, panel_name, None, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_genes_by_panel(
            ReportEventType.tiered, panel_name, None, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

    def test_get_variants_by_genomic_region(self):

        assembly = Assembly.GRCh38
        chromosome = 7
        start = 1000000
        end = 2000000

        # gets variants
        results = self.report_events.get_variants_by_genomic_region(
            Program.rare_disease, ReportEventType.tiered,
            assembly, chromosome, start, end, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_variants_by_genomic_region(
            Program.rare_disease, ReportEventType.tiered,
            assembly, chromosome, start, end, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets phenotypes
        results = self.report_events.get_phenotypes_by_genomic_region(
            Program.rare_disease, ReportEventType.tiered,
            assembly, chromosome, start, end, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_phenotypes_by_genomic_region(
            Program.rare_disease, ReportEventType.tiered,
            assembly, chromosome, start, end, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets genes
        results = self.report_events.get_genes_by_genomic_region(
            Program.rare_disease, ReportEventType.tiered,
            assembly, chromosome, start, end, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_genes_by_genomic_region(
            Program.rare_disease, ReportEventType.tiered,
            assembly, chromosome, start, end, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

    def test_get_all_panels(self):

        panels = self.panels.get_all_panels()
        self.assertTrue(panels is not None)
        self.assertTrue(isinstance(panels, list))

        panels = self.panels.get_all_panels(include_versions=True)
        self.assertTrue(panels is not None)
        self.assertTrue(isinstance(panels, list))

    def test_get_panel_summary(self):

        panels = self.panels.get_panels_summary(Program.rare_disease)
        self.assertTrue(panels is not None)
        self.assertTrue(isinstance(panels, dict))

        panels = self.panels.get_panels_summary(Program.cancer)
        self.assertTrue(panels is not None)
        self.assertTrue(isinstance(panels, dict))

    def test_cases_get_by_gene_id(self):

        gene_id = "ENSG00000130826"

        # gets variants
        results = self.cases.get_variants_by_gene_id(
            Program.rare_disease, Assembly.GRCh38,
            gene_id, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_variants_by_gene_id(
            Program.rare_disease, Assembly.GRCh38,
            gene_id, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets phenotypes
        results = self.cases.get_phenotypes_by_gene_id(
            Program.rare_disease, Assembly.GRCh38,
            gene_id, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_phenotypes_by_gene_id(
            Program.rare_disease, Assembly.GRCh38,
            gene_id, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

    def test_get_cases_variants_by_transcript_id(self):

        tx_id = "ENST00000426673"

        # gets variants
        results = self.cases.get_variants_by_transcript_id(
            Program.rare_disease, Assembly.GRCh38,
            tx_id, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_variants_by_transcript_id(
            Program.rare_disease, Assembly.GRCh38,
            tx_id, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets phenotypes
        results = self.cases.get_phenotypes_by_transcript_id(
            Program.rare_disease, Assembly.GRCh38,
            tx_id, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_phenotypes_by_transcript_id(
            Program.rare_disease, Assembly.GRCh38,
            tx_id, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

    def test_get_cases_variants_by_gene_symbol(self):

        gene_symbol = "BRCA1"

        # gets variants
        results = self.cases.get_variants_by_gene_symbol(
            Program.rare_disease, Assembly.GRCh38,
            gene_symbol, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_variants_by_gene_symbol(
            Program.rare_disease, Assembly.GRCh38,
            gene_symbol, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets phenotypes
        results = self.cases.get_phenotypes_by_gene_symbol(
            Program.rare_disease, Assembly.GRCh38,
            gene_symbol, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_phenotypes_by_gene_symbol(
            Program.rare_disease, Assembly.GRCh38,
            gene_symbol, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

    def test_get_cases_variants_by_panel(self):

        panel_name = "cakut"

        # gets variants
        results = self.cases.get_variants_by_panel(panel_name, None, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_variants_by_panel(panel_name, None, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets phenotypes
        results = self.cases.get_phenotypes_by_panel(panel_name, None, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_phenotypes_by_panel(panel_name, None, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets genes
        results = self.cases.get_genes_by_panel(panel_name, None, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_genes_by_panel(panel_name, None, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

    def test_get_cases_variants_by_genomic_region(self):

        assembly = Assembly.GRCh38
        chromosome = 7
        start = 1000000
        end = 2000000

        # gets variants
        results = self.cases.get_variants_by_genomic_region(
            Program.rare_disease,
            assembly, chromosome, start, end, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_variants_by_genomic_region(
            Program.rare_disease,
            assembly, chromosome, start, end, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets phenotypes
        results = self.cases.get_phenotypes_by_genomic_region(
            Program.rare_disease,
            assembly, chromosome, start, end, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_phenotypes_by_genomic_region(
            Program.rare_disease,
            assembly, chromosome, start, end, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets genes
        results = self.cases.get_genes_by_genomic_region(
            Program.rare_disease,
            assembly, chromosome, start, end, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_genes_by_genomic_region(
            Program.rare_disease,
            assembly, chromosome, start, end, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

    def test_get_variant_by_id(self):

        identifier = "GRCh38: 9: 110303682:C:G"

        # gets variant
        variant = self.variants.get_variant_by_id(identifier=identifier)
        self.assertTrue(variant is not None)
        self.assertTrue(isinstance(variant, Variant))

        # non existing variant
        try:
            variant = self.variants.get_variant_by_id(identifier='whatever')
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
