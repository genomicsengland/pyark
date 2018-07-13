import re
import logging
from pandas.io.json import json_normalize
from pyark.rest_client import RestClient


class CvaClient(RestClient):

    regx = re.compile("^test_", re.IGNORECASE)

    ENDPOINT_BASE = "cva/api/0"

    LIMIT_PARAM = 'limit'
    MARKER_PARAM = 'marker'
    LIMIT_HEADER = 'X-Pagination-Limit'
    MARKER_HEADER = 'X-Pagination-Marker'

    # mocked data endpoints
    TIERED_VARIANTS_INJECT_RD = "mocked-data/rd/tiered-variant-inject"
    CANDIDATE_VARIANTS_INJECT_RD = "mocked-data/rd/candidate-variant-inject"
    REPORTED_VARIANTS_INJECT_RD = "mocked-data/rd/reported-variant-inject"
    TIERED_VARIANTS_INJECT_CANCER = "mocked-data/cancer/tiered-variant-inject"
    CANDIDATE_VARIANTS_INJECT_CANCER = "mocked-data/cancer/candidate-variant-inject"
    REPORTED_VARIANTS_INJECT_CANCER = "mocked-data/cancer/reported-variant-inject"
    # post report events endpoints
    TIERED_VARIANT_RD_POST = "tiered-variants/rd"
    CANDIDATE_VARIANT_RD_POST = "candidate-variants/rd"
    REPORTED_VARIANT_RD_POST = "reported-variants/rd"
    EXIT_QUESTIONAIRES_RD_POST = "exit-questionnaires/rd"
    TIERED_VARIANT_CANCER_POST = "tiered-variants/cancer"
    CANDIDATE_VARIANT_CANCER_POST = "candidate-variants/cancer"
    REPORTED_VARIANT_CANCER_POST = "reported-variants/cancer"
    EXIT_QUESTIONAIRES_CANCER_POST = "exit-questionnaires/cancer"
    # post other entities
    PEDIGREE_POST = "pedigrees"
    PARTICIPANT_POST = "participants"
    # other entities
    TRANSACTIONS = "transactions"
    REPORT_EVENTS = "report-events"
    VARIANTS = "variants"
    EVIDENCES = "evidences"
    # authentication endpoint
    AUTHENTICATION = "authentication"

    def __init__(self, url_base, token=None, user=None, password=None,
                 disable_validation=True, disable_annotation=False):

        if not (token or (user and password is not None)):
            logging.error("Credentials are required. Either token or user/password.")
            raise ValueError("Missing credentials")
        RestClient.__init__(self, url_base, self.ENDPOINT_BASE)
        self.disable_validation = disable_validation
        self.disable_annotation = disable_annotation
        self.push_data_params = {'disable_validation': self.disable_validation,
                                 'disable_annotation': self.disable_annotation}
        self.token = "Bearer {}".format(token.replace("Bearer ", "")) if token else None
        self.user = user
        self.password = password
        if self.token or (self.user is not None and self.password is not None):
            self.set_authenticated_header()
        # initialise subclients
        self.report_events_client = None
        self.panels_client = None
        self.cases_client = None
        self.variants_client = None
        self.lift_overs_client = None
        self.data_intake_client = None
        self.transactions_client = None

    def get_token(self):
        results, _ = self.post(self.AUTHENTICATION, payload={
            'username': self.user,
            'password': self.password
        })
        return "Bearer {}".format(results[0]['token'])

    def post(self, endpoint, payload, params={}, session=True):
        response, headers = super(CvaClient, self).post(endpoint, payload, params, session)
        return CvaClient.parse_result(response), CvaClient.build_next_page_params(headers)

    def get(self, endpoint, params={}, session=True):
        response, headers = super(CvaClient, self).get(endpoint, params, session)
        return CvaClient.parse_result(response), CvaClient.build_next_page_params(headers)

    def delete(self, endpoint, params={}):
        response, headers = super(CvaClient, self).delete(endpoint, params)
        return CvaClient.parse_result(response), CvaClient.build_next_page_params(headers)

    def report_events(self):
        """

        :return:
        :rtype: ReportEventsClient
        """
        # NOTE: this import needs to be here due to circular imports
        import pyark.subclients.report_events_client
        if self.report_events_client is None:
            # initialise subclients
            self.report_events_client = pyark.subclients.report_events_client.ReportEventsClient(
                self.url_base, self.token)
        return self.report_events_client

    def panels(self):
        """

        :return:
        :rtype: PanelsClient
        """
        # NOTE: this import needs to be here due to circular imports
        import pyark.subclients.panels_client
        if self.panels_client is None:
            # initialise subclients
            self.panels_client = pyark.subclients.panels_client.PanelsClient(self.url_base, self.token)
        return self.panels_client

    def cases(self):
        """

        :return:
        :rtype: CasesClient
        """
        # NOTE: this import needs to be here due to circular imports
        import pyark.subclients.cases_client
        if self.cases_client is None:
            # initialise subclients
            self.cases_client = pyark.subclients.cases_client.CasesClient(
                self.url_base, self.token)
        return self.cases_client

    def variants(self):
        """

        :return:
        :rtype: VariantsClient
        """
        # NOTE: this import needs to be here due to circular imports
        import pyark.subclients.variants_client
        if self.variants_client is None:
            # initialise subclients
            self.variants_client = pyark.subclients.variants_client.VariantsClient(
                self.url_base, self.token)
        return self.variants_client

    def transactions(self):
        """

        :return:
        :rtype: VariantsClient
        """
        # NOTE: this import needs to be here due to circular imports
        import pyark.subclients.transactions_client
        if self.transactions_client is None:
            # initialise subclients
            self.transactions_client = pyark.subclients.transactions_client.TransactionsClient(
                self.url_base, self.token)
        return self.transactions_client

    def lift_overs(self):
        """

        :return:
        :rtype: LiftOverClient
        """
        # NOTE: this import needs to be here due to circular imports
        import pyark.subclients.lift_over_client
        if self.lift_overs_client is None:
            # initialise subclients
            self.lift_overs_client = pyark.subclients.lift_over_client.LiftOverClient(
                self.url_base, self.token)
        return self.lift_overs_client

    def data_intake(self):
        """

        :return:
        :rtype: DataIntakeClient
        """
        # NOTE: this import needs to be here due to circular imports
        import pyark.subclients.data_intake_client
        if self.data_intake_client is None:
            # initialise subclients
            self.data_intake_client = pyark.subclients.data_intake_client.DataIntakeClient(
                self.url_base, self.token)
        return self.data_intake_client

    @staticmethod
    def build_next_page_params(headers):
        next_page_params = {}
        limit = headers.get(CvaClient.LIMIT_HEADER, None)
        marker = headers.get(CvaClient.MARKER_HEADER, None)
        if marker:
            next_page_params[CvaClient.LIMIT_PARAM] = limit
            next_page_params[CvaClient.MARKER_PARAM] = marker
        return next_page_params

    @staticmethod
    def parse_result(response):
        logging.info("Response time : {} ms".format(response.get('time', None)))
        error = response.get('error', None)
        if error:
            logging.error(error)
            raise ValueError(error)
        warning = response.get('warning', None)
        if warning:
            logging.warning(warning)
        if 'response' in response and len(response['response']) > 0 and 'result' in response['response'][0]:
            return response['response'][0]['result']
        else:
            return []

    @staticmethod
    def results2dict(results):
        """
        Flattens results dictionary making the value in '_id' the key and the rest the value
        :param results:
        :type results: dict
        :return:
        :rtype: dict
        """
        return dict(map(lambda x: (x['_id'], {key: x[key] for key in x if key != '_id'}), results))

    @staticmethod
    def results2list(results):
        """
        Flattens results dictionary into a list of those elements in the key '_id'
        :param results:
        :type results: dict
        :return:
        :rtype: list
        """
        return list(map(lambda x: x['_id'], results))

    def get_aggregation_query(self, path, include_aggregations=False, params={}):
        """

        :param path:
        :type path: list
        :param include_aggregations:
        :type include_aggregations: bool
        :param params:
        :type params: dict
        :return:
        :rtype: list
        """
        if not params:
            params = {}
        params['include_aggregations'] = include_aggregations
        results, _ = self.get("/".join(path), params=params)
        if include_aggregations:
            return CvaClient.results2dict(results)
        else:
            return CvaClient.results2list(results)

    def render_single_result(self, results, as_data_frame=True):
        first = results[0]
        return self.render(first, as_data_frame)

    @staticmethod
    def render(results, as_data_frame=True):
        if as_data_frame:
            return json_normalize(results)
        else:
            return results
