import logging
import os
from unittest import TestCase

import pandas as pd
from mock import patch
from protocols.protocol_7_0.cva import ReportEventType, Assembly, PedigreeInjectRD, CancerParticipantInject, \
    EvidenceEntryAndVariants, EvidenceEntry, Property, EvidenceSource, Actions, Therapy, DrugResponse, GenomicFeature, \
    FeatureTypes, VariantCoordinates, VariantsCoordinates, Penetrance, DrugResponseClassification
from protocols.protocol_7_0.reports import Program
from protocols.util import dependency_manager
from protocols.util.factories.avro_factory import GenericFactoryAvro
from requests import ConnectionError

from pyark.cva_client import CvaClient
from pyark.errors import CvaClientError, CvaServerError

import uuid


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
        self.cva = CvaClient(self.CVA_URL_BASE, user=self.GEL_USER, password=self.GEL_PASSWORD, retries=10)
        self.report_events = self.cva.report_events()
        self.entities = self.cva.entities()
        self.cases = self.cva.cases()
        self.pedigrees = self.cva.pedigrees()
        self.variants = self.cva.variants()
        self.data_intake = self.cva.data_intake()

    def test_get_case(self):

        case_id = "1000"
        case_version = 1

        # gets case
        result = self.cases.get_case(case_id, case_version)
        self.assertTrue(result is not None)
        self.assertTrue(isinstance(result, dict))

        # gets pedigree
        result = self.cases.get_case(case_id, case_version, as_data_frame=True)
        self.assertTrue(result is not None)
        self.assertTrue(isinstance(result, pd.DataFrame))

    def test_get_pedigree(self):

        case_id = "2020"
        case_version = 1

        # gets pedigree
        result = self.pedigrees.get_pedigree(case_id, case_version)
        self.assertTrue(result is not None)
        self.assertTrue(isinstance(result, dict))

        # gets pedigree
        result = self.pedigrees.get_pedigree(case_id, case_version, as_data_frame=True)
        self.assertTrue(result is not None)
        self.assertTrue(isinstance(result, pd.DataFrame))

    def test_get_report_events(self):

        all_report_events = self.report_events.get_report_events(caseId='1000', limit=2)
        re_count = 0
        for batch_report_events in all_report_events:
            self.assertIsNotNone(batch_report_events)
            re_count += 1
            if re_count == 5:
                break
        self.assertEqual(re_count, 5)

    def test_count_report_events(self):

        count = self.report_events.count()
        self.assertIsInstance(count, int)

    def test_count_variants(self):

        count = self.variants.count()
        self.assertIsInstance(count, int)

    def test_get_variants(self):

        all_variants = self.variants.get_variants(limit=2)
        re_count = 0
        for batch_variants in all_variants:
            self.assertIsNotNone(batch_variants)
            re_count += 1
            if re_count == 5:
                break
        self.assertEqual(re_count, 5)

    def test_get_by_gene_id(self):

        gene_id = self._get_random_gene()

        # gets variants
        results = self.report_events.get_variants_by_gene_id(
            program=Program.rare_disease, type=ReportEventType.genomics_england_tiering,
            assembly=Assembly.GRCh38, gene_id=gene_id, includeAggregations=False)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

        results = self.report_events.get_variants_by_gene_id(
            program=Program.rare_disease, type=ReportEventType.genomics_england_tiering,
            assembly=Assembly.GRCh38, gene_id=gene_id, includeAggregations=True)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

    def test_get_variants_by_gene_symbol(self):
        gene_symbol = self._get_random_gene()

        # gets variants
        results = self.report_events.get_variants_by_gene_symbol(
            program=Program.rare_disease, type=ReportEventType.genomics_england_tiering,
            assembly=Assembly.GRCh38, gene_symbol=gene_symbol, includeAggregations=False)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

        results = self.report_events.get_variants_by_gene_symbol(
            program=Program.rare_disease, type=ReportEventType.genomics_england_tiering,
            assembly=Assembly.GRCh38, gene_symbol=gene_symbol, includeAggregations=True)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

    def test_get_variants_by_genomic_region(self):

        assembly = Assembly.GRCh38
        chromosome = 7
        start = 1000000
        end = 1010000

        # gets variants
        results = self.report_events.get_variants_by_genomic_region(
            program=Program.rare_disease, type=ReportEventType.genomics_england_tiering,
            assembly=assembly, chromosome=chromosome, start=start, end=end, includeAggregations=False)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

        results = self.report_events.get_variants_by_genomic_region(
            program=Program.rare_disease, type=ReportEventType.genomics_england_tiering,
            assembly=assembly, chromosome=chromosome, start=start, end=end, includeAggregations=True)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

        # gets genes
        results = self.report_events.get_genes_by_genomic_region(
            program=Program.rare_disease, type=ReportEventType.genomics_england_tiering,
            assembly=assembly, chromosome=chromosome, start=start, end=end, includeAggregations=False)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

        results = self.report_events.get_genes_by_genomic_region(
            program=Program.rare_disease, type=ReportEventType.genomics_england_tiering,
            assembly=assembly, chromosome=chromosome, start=start, end=end, includeAggregations=True)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

    def test_get_all_panels(self):
        panels = self.entities.get_all_panels()
        self.assertIsNotNone(panels)
        self.assertIsInstance(panels, pd.Series)

    def test_get_panel_summary(self):

        panels = self.entities.get_panels_summary(program=Program.rare_disease)
        self.assertIsNotNone(panels)
        self.assertIsInstance(panels, list)

        panels = self.entities.get_panels_summary(program=Program.cancer, as_data_frame=True)
        self.assertIsNotNone(panels)
        self.assertIsInstance(panels, pd.DataFrame)

    def test_get_disorder_summary(self):

        disorders = self.entities.get_disorders_summary(program=Program.rare_disease)
        self.assertIsNotNone(disorders)
        self.assertIsInstance(disorders, list)

        disorders = self.entities.get_disorders_summary(program=Program.cancer, as_data_frame=True)
        self.assertIsNotNone(disorders)
        self.assertIsInstance(disorders, pd.DataFrame)

    def test_get_gene_summary(self):

        genes = self.entities.get_genes_summary(program=Program.rare_disease)
        self.assertIsNotNone(genes)
        self.assertIsInstance(genes, list)

        genes = self.entities.get_genes_summary(program=Program.cancer, as_data_frame=True)
        self.assertIsNotNone(genes)
        self.assertIsInstance(genes, pd.DataFrame)

    def test_get_phenotypes_summary(self):

        phenotypes = self.entities.get_phenotypes(program=Program.rare_disease)
        self.assertIsNotNone(phenotypes)
        self.assertIsInstance(phenotypes, list)

        phenotypes = self.entities.get_phenotypes(program=Program.cancer, as_data_frame=True)
        self.assertIsNotNone(phenotypes)
        self.assertIsInstance(phenotypes, pd.DataFrame)

    def test_cases_get_by_gene_id(self):

        gene_id = self._get_random_gene()

        # gets variants
        results = self.cases.get_variants_by_gene_id(
            program=Program.rare_disease, assembly=Assembly.GRCh38,
            gene_id=gene_id, includeAggregations=False)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

        results = self.cases.get_variants_by_gene_id(
            program=Program.rare_disease, assembly=Assembly.GRCh38,
            gene_id=gene_id, includeAggregations=True)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

    def test_get_cases(self):

        all_cases = self.cases.get_cases({'limit': 2})
        case_count = 0
        for batch_cases in all_cases:
            self.assertIsNotNone(batch_cases)
            # self.assertEqual(len(batch_report_events), 10)
            # logging.info("Returned {} report events".format(len(batch_report_events)))
            case_count += 1
            if case_count == 5:
                break
        self.assertEqual(case_count, 5)

    def test_count_cases(self):

        count = self.cases.count()
        self.assertIsInstance(count, int)

    def test_get_cases_variants_by_gene_symbol(self):

        gene_symbol = self._get_random_gene()

        # gets variants
        results = self.cases.get_variants_by_gene_symbol(
            program=Program.rare_disease, assembly=Assembly.GRCh38, gene_symbol=gene_symbol, includeAggregations=False)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

        results = self.cases.get_variants_by_gene_symbol(
            program=Program.rare_disease, assembly=Assembly.GRCh38, gene_symbol=gene_symbol, includeAggregations=True)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

    def test_get_cases_variants_by_genomic_region(self):

        assembly = Assembly.GRCh38
        chromosome = 7
        start = 1000000
        end = 2000000

        # gets variants
        results = self.cases.get_variants_by_genomic_region(
            program=Program.rare_disease, assembly=assembly, chromosome=chromosome, start=start, end=end,
            includeAggregations=False)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

        results = self.cases.get_variants_by_genomic_region(
            program=Program.rare_disease, assembly=assembly, chromosome=chromosome, start=start, end=end,
            includeAggregations=True)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

        # gets genes
        results = self.cases.get_genes_by_genomic_region(
            program=Program.rare_disease, assembly=assembly, chromosome=chromosome, start=start, end=end,
            includeAggregations=False)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

        results = self.cases.get_genes_by_genomic_region(
            program=Program.rare_disease, assembly=assembly, chromosome=chromosome, start=start, end=end,
            includeAggregations=True)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

    def test_get_similar_cases_by_case(self):

        case_id, case_version = self._get_random_case()

        results = self.cases.get_similar_cases_by_case(
            case_id=case_id, case_version=case_version, phenotypeSimilarityMetric="LIN")
        if results:
            self.assertIsInstance(results, list)

        results = self.cases.get_similar_cases_by_case(
            case_id=case_id, case_version=case_version, phenotypeSimilarityMetric="LIN", limit=5)
        if results:
            self.assertIsInstance(results, list)
            self.assertTrue(len(results) <= 5)

        results = self.cases.get_similar_cases_by_case(
            case_id=case_id, case_version=case_version, phenotypeSimilarityMetric="RESNIK")
        if results:
            self.assertIsInstance(results, list)

        results = self.cases.get_similar_cases_by_case(
            case_id=case_id, case_version=case_version, phenotypeSimilarityMetric="JACCARD")
        if results:
            self.assertIsInstance(results, list)

    def test_get_similar_cases_by_phenotypes(self):

        phenotypes = ["HP:0000006", "HP:0003186", "HP:0002365"]

        results = self.cases.get_similar_cases_by_phenotypes(
            phenotypes=phenotypes, phenotypeSimilarityMetric="LIN")
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

        results = self.cases.get_similar_cases_by_phenotypes(
            phenotypes=phenotypes, phenotypeSimilarityMetric="LIN", limit=5)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)
        self.assertTrue(len(results) == 5)

        results = self.cases.get_similar_cases_by_phenotypes(
            phenotypes=phenotypes, phenotypeSimilarityMetric="RESNIK")
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

        results = self.cases.get_similar_cases_by_phenotypes(
            phenotypes=phenotypes, phenotypeSimilarityMetric="JACCARD")
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

    def test_get_shared_variants_cases(self):
        case_id, case_version = self._get_random_case()

        results = self.cases.get_shared_variants_cases_by_case(
            case_id=case_id, case_version=case_version, report_event_type=ReportEventType.genomics_england_tiering)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

        results = self.cases.get_shared_variants_cases_by_case(
            case_id=case_id, case_version=case_version, report_event_type=ReportEventType.reported)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

        results = self.cases.get_shared_variants_cases_by_case(
            case_id=case_id, case_version=case_version, report_event_type=ReportEventType.questionnaire)
        # self.assertIsNotNone(results)
        # self.assertIsInstance(results, list)

    def test_get_shared_gene_cases(self):
        case_id, case_version = self._get_random_case()

        results = self.cases.get_shared_genes_cases_by_case(
            case_id=case_id, case_version=case_version, report_event_type=ReportEventType.genomics_england_tiering)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

        results = self.cases.get_shared_genes_cases_by_case(
            case_id=case_id, case_version=case_version, report_event_type=ReportEventType.reported)
        self.assertIsNotNone(results)
        self.assertIsInstance(results, list)

        results = self.cases.get_shared_genes_cases_by_case(
            case_id=case_id, case_version=case_version, report_event_type=ReportEventType.questionnaire)
        # NOTE: there are no values
        # self.assertIsNotNone(results)
        # self.assertIsInstance(results, list)

    def test_get_variant_by_id(self):

        identifier = "GRCh38: 9: 110303682:C:G"

        # gets variant
        variant = self.variants.get_variant_by_id(identifier=identifier)
        # self.assertIsNotNone(variant)
        # self.assertIsInstance(variant, Variant)

        # non existing variant
        # variant = self.variants.get_variant_by_id(identifier='whatever')
        # self.assertFalse(variant)

    def test_get_variants_by_id(self):

        identifiers = ["GRCh38: 9: 110303682:C:G", "GRCh38: 4:  56810156:G:A", "GRCh38:12:  51346624:A:C"]
        variants = self.variants.get_variants_by_id(identifiers=identifiers)
        self.assertIsNotNone(variants)
        self.assertIsInstance(variants, dict)
        self.assertTrue(len(variants) == len(identifiers))
        # [self.assertIsNotNone(variants[v]) for v in identifiers]

        non_existing_identifiers = ['whatever', 'this', 'that']
        variants = self.variants.get_variants_by_id(identifiers=non_existing_identifiers)
        self.assertIsNotNone(variants)
        self.assertIsInstance(variants, dict)
        self.assertTrue(len(variants) == len(non_existing_identifiers))
        [self.assertTrue(variants[v] is None) for v in non_existing_identifiers]

        mixed_identifiers = ['whatever', "GRCh38: 9: 110303682:C:G"]
        variants = self.variants.get_variants_by_id(identifiers=mixed_identifiers)
        self.assertIsNotNone(variants)
        self.assertIsInstance(variants, dict)
        self.assertTrue(len(variants) == len(mixed_identifiers))
        # self.assertTrue(variants[mixed_identifiers[0]] is None)
        # self.assertIsNotNone(variants[mixed_identifiers[1]])

    def test_post_pedigree(self):
        self._test_post(PedigreeInjectRD, self.data_intake.post_pedigree)

    def test_post_participant(self):
        self._test_post(CancerParticipantInject, self.data_intake.post_participant)

    def test_get_transactions(self):
        client = self.cva.transactions()
        tx = client.get_transactions(params={'limit': 1}).next()
        self.assertTrue(client.get_transaction(tx.id))
        try:
            self.assertTrue(client.retry_transaction(tx.id))
        except CvaServerError as e:
            # this should be a Done transaction so you can't retry it
            self.assertTrue("cannot be retried" in e.message)

    def test_count_transactions(self):

        count = self.cva.transactions().count()
        self.assertIsInstance(count, int)

    def test_get_transaction_status_only(self):
        client = self.cva.transactions()
        tx = client.get_transactions(params={'limit': 1}).next()
        self.assertEqual(client.get_transaction(tx.id, just_return_status=True), 'DONE')

    def test_get_transaction_status_only_fails_if_no_results(self):
        client = self.cva.transactions()
        self.assertRaises(
            CvaClientError,
            lambda: client.get_transaction("notreal", just_return_status=True)
        )

    def test_errors_if_cva_down(self):
        self.assertRaises(
            ConnectionError,
            lambda: CvaClient("https://nowhere.invalid", user='u', password='p', retries=2).entities().get_all_panels()
        )

    @patch('requests.sessions.Session.get')
    @patch('requests.sessions.Session.post')
    def test_errors_if_4xx(self, post, get):
        self._mock_panels_to_return(get, post, 400)
        self.assertRaises(
            CvaClientError,
            lambda: CvaClient("https://nowhere.invalid", user='u', password='p').entities().get_all_panels()
        )

    @patch('requests.sessions.Session.get')
    @patch('requests.sessions.Session.post')
    def test_errors_if_5xx(self, post, get):
        self._mock_panels_to_return(get, post, 500)
        self.assertRaises(
            CvaServerError,
            lambda: CvaClient("https://nowhere.invalid", user='u', password='p').entities().get_all_panels()
        )

    @patch('requests.sessions.Session.get')
    @patch('requests.sessions.Session.post')
    def test_returns_empty_if_no_results(self, post, get):
        self._mock_panels_to_return(get, post, 200)
        self.assertEqual(0,
                         CvaClient("https://nowhere.invalid", user='u', password='p').entities().get_all_panels().size)

    def test_gets_evidence(self):
        model = create_example_evidence()
        model.evidenceEntry.source.name = str(uuid.uuid1())
        model.evidenceEntry.source.version = str(uuid.uuid1())

        self.cva.evidences().post_evidences(model)

        evidences = self.cva.evidences().get_evidences(
            model.evidenceEntry.source.name,
            version=model.evidenceEntry.source.version
        )
        self.assertTrue(list(evidences), "expected some evidence")

    @staticmethod
    def _mock_panels_to_return(get, post, status_code):
        auth_response = MockResponse(status_code, {'response': [{'result': [{'token': 'xyz'}]}]})
        post.return_value = auth_response
        response = MockResponse(status_code, {})
        get.return_value = response

    def _test_post(self, clazz, post_function):
        model = GenericFactoryAvro.get_factory_avro(
            clazz=clazz,
            version=dependency_manager.VERSION_70,
            fill_nullables=False,
        ).create()

        response = post_function(model)
        # this is stronger than it looks because post checks for errors
        self.assertIsNotNone(response)
        return response

    def _get_random_case(self):
        example_case = self.random_case(lambda x: x)
        case_id = example_case['identifier']
        case_version = example_case['version']
        return case_id, case_version

    def _get_random_panel(self):
        return self.random_case(lambda case: case['reportEventsAnalysisPanels'][0]['panelName'])

    def _get_random_gene(self):
        return self.random_case(lambda case: case['reportedGenes'][0])

    def random_case(self, extractor):
        for case in self.cases.get_cases(hasExitQuestionnaire=True, hasClinicalReport=True):
            for c in case:
                try:
                    extracted = extractor(c)
                    if extracted:
                        return extracted
                except:
                    pass


class MockResponse:
    def __init__(self, status_code, json_dict):
        self.status_code = status_code
        self.json_dict = json_dict
        self.content = str(json_dict)
        self.text = str(json_dict)
        self.headers = {}

    @staticmethod
    def get(key, default):
        return None

    def json(self):
        return self.json_dict


def create_example_evidence():
    coordinates = coordinate()
    marker_coordinates = marker_coordinate()

    genomic_feature = GenomicFeature(
        featureType=FeatureTypes.transcript,
        ensemblId="ENST00000370192.7"
    )

    actions = action()

    source = EvidenceSource(
        date="today",
        name="genomics-england-phamacogenomics",
        version="v1.0"
    )

    pharmgkb_id = Property(
        name="PharmGKB",
        value="PA166153760"
    )

    return EvidenceEntryAndVariants(
        evidenceEntry=EvidenceEntry(
            source=source,
            ethnicity='Z',
            genomicFeatures=[genomic_feature],
            heritable_trait=[],
            penetrance=Penetrance.complete,
            additionalProperties=[pharmgkb_id]
        ),
        variantsCoordinates=VariantsCoordinates(variants=[coordinates]),
        markersCoordinates=VariantsCoordinates(variants=[marker_coordinates]),
        actions=actions
    )


def action():
    return Actions(
        therapies=[
            Therapy(
                drugResponse=[DrugResponse(
                    TreatmentAgent="the drug",
                    drugResponseClassification=DrugResponseClassification.increased_monitoring
                )],
                variantActionable=True,
                referenceUrl="https://something.com/db.html",
                conditions=[]
            )
        ]
    )


def marker_coordinate():
    marker_coordinates = VariantCoordinates(
        assembly=Assembly.GRCh38, reference='G', alternate='T', chromosome='1', position=99450058
    )
    return marker_coordinates


def coordinate():
    coordinates = VariantCoordinates(
        assembly=Assembly.GRCh38, reference='C', alternate='T', chromosome='1', position=97450058
    )
    return coordinates
