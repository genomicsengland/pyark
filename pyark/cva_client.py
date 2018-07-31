import re
import logging
from pandas.io.json import json_normalize
from pyark.rest_client import RestClient
import multiprocessing


class CvaClient(RestClient):

    _regx = re.compile("^test_", re.IGNORECASE)

    _ENDPOINT_BASE = "cva/api/0"

    _LIMIT_PARAM = 'limit'
    _MARKER_PARAM = 'marker'
    _LIMIT_HEADER = 'X-Pagination-Limit'
    _MARKER_HEADER = 'X-Pagination-Marker'

    # authentication endpoint
    _AUTHENTICATION_ENDPOINT = "authentication"

    def __init__(self, url_base, token=None, user=None, password=None,
                 disable_validation=True, disable_annotation=False):

        if not (token or (user and password is not None)):
            logging.error("Credentials are required. Either token or user/password.")
            raise ValueError("Missing credentials")
        RestClient.__init__(self, url_base, self._ENDPOINT_BASE)
        self._disable_validation = disable_validation
        self._disable_annotation = disable_annotation
        self._push_data_params = {'disable_validation': self._disable_validation,
                                 'disable_annotation': self._disable_annotation}
        self._token = "Bearer {}".format(token.replace("Bearer ", "")) if token else None
        self._user = user
        self._password = password
        if self._token or (self._user is not None and self._password is not None):
            self._set_authenticated_header()
        # initialise subclients
        self._report_events_client = None
        self._panels_client = None
        self._cases_client = None
        self._pedigrees_client = None
        self._variants_client = None
        self._lift_overs_client = None
        self._data_intake_client = None
        self._transactions_client = None

    def _get_token(self):
        results, _ = self._post(self._AUTHENTICATION_ENDPOINT, payload={
            'username': self._user,
            'password': self._password
        })
        return "Bearer {}".format(results[0]['token'])

    def _post(self, endpoint, payload, params={}, session=True):
        response, headers = super(CvaClient, self)._post(endpoint, payload, params, session)
        return CvaClient._parse_result(response), CvaClient._build_next_page_params(headers)

    def _get(self, endpoint, params={}, session=True):
        response, headers = super(CvaClient, self)._get(endpoint, params, session)
        return CvaClient._parse_result(response), CvaClient._build_next_page_params(headers)

    def _delete(self, endpoint, params={}):
        response, headers = super(CvaClient, self)._delete(endpoint, params)
        return CvaClient._parse_result(response), CvaClient._build_next_page_params(headers)

    @staticmethod
    def run_parallel_requests(method, parameters):
        """
        :type method: function
        :type parameters: list
        :rtype: object
        """
        pool = multiprocessing.Pool(processes=10)
        results = dict(pool.map(method, parameters))
        pool.close()
        pool.join()
        return results

    def report_events(self):
        """

        :return:
        :rtype: ReportEventsClient
        """
        # NOTE: this import needs to be here due to circular imports
        import pyark.subclients.report_events_client
        if self._report_events_client is None:
            # initialise subclients
            self._report_events_client = pyark.subclients.report_events_client.ReportEventsClient(
                self._url_base, self._token)
        return self._report_events_client

    def panels(self):
        """

        :return:
        :rtype: PanelsClient
        """
        # NOTE: this import needs to be here due to circular imports
        import pyark.subclients.panels_client
        if self._panels_client is None:
            # initialise subclients
            self._panels_client = pyark.subclients.panels_client.PanelsClient(self._url_base, self._token)
        return self._panels_client

    def cases(self):
        """

        :return:
        :rtype: CasesClient
        """
        # NOTE: this import needs to be here due to circular imports
        import pyark.subclients.cases_client
        if self._cases_client is None:
            # initialise subclients
            self._cases_client = pyark.subclients.cases_client.CasesClient(
                self._url_base, self._token)
        return self._cases_client

    def pedigrees(self):
        """

        :return:
        :rtype: CasesClient
        """
        # NOTE: this import needs to be here due to circular imports
        import pyark.subclients.cases_client
        if self._pedigrees_client is None:
            # initialise subclients
            self._pedigrees_client = pyark.subclients.pedigrees_client.PedigreesClient(
                self._url_base, self._token)
        return self._pedigrees_client

    def variants(self):
        """

        :return:
        :rtype: VariantsClient
        """
        # NOTE: this import needs to be here due to circular imports
        import pyark.subclients.variants_client
        if self._variants_client is None:
            # initialise subclients
            self._variants_client = pyark.subclients.variants_client.VariantsClient(
                self._url_base, self._token)
        return self._variants_client

    def transactions(self):
        """

        :return:
        :rtype: VariantsClient
        """
        # NOTE: this import needs to be here due to circular imports
        import pyark.subclients.transactions_client
        if self._transactions_client is None:
            # initialise subclients
            self._transactions_client = pyark.subclients.transactions_client.TransactionsClient(
                self._url_base, self._token)
        return self._transactions_client

    def lift_overs(self):
        """

        :return:
        :rtype: LiftOverClient
        """
        # NOTE: this import needs to be here due to circular imports
        import pyark.subclients.lift_over_client
        if self._lift_overs_client is None:
            # initialise subclients
            self._lift_overs_client = pyark.subclients.lift_over_client.LiftOverClient(
                self._url_base, self._token)
        return self._lift_overs_client

    def data_intake(self):
        """

        :return:
        :rtype: DataIntakeClient
        """
        # NOTE: this import needs to be here due to circular imports
        import pyark.subclients.data_intake_client
        if self._data_intake_client is None:
            # initialise subclients
            self._data_intake_client = pyark.subclients.data_intake_client.DataIntakeClient(
                self._url_base, self._token)
        return self._data_intake_client

    @staticmethod
    def _build_next_page_params(headers):
        next_page_params = {}
        limit = headers.get(CvaClient._LIMIT_HEADER, None)
        marker = headers.get(CvaClient._MARKER_HEADER, None)
        if marker:
            next_page_params[CvaClient._LIMIT_PARAM] = limit
            next_page_params[CvaClient._MARKER_PARAM] = marker
        return next_page_params

    @staticmethod
    def _parse_result(response):
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
    def _results2dict(results):
        """
        Flattens results dictionary making the value in '_id' the key and the rest the value
        :param results:
        :type results: dict
        :return:
        :rtype: dict
        """
        return dict(map(lambda x: (x['_id'], {key: x[key] for key in x if key != '_id'}), results))

    @staticmethod
    def _results2list(results):
        """
        Flattens results dictionary into a list of those elements in the key '_id'
        :param results:
        :type results: dict
        :return:
        :rtype: list
        """
        return list(map(lambda x: x['_id'], results))

    def _get_aggregation_query(self, path, include_aggregations=False, params={}):
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
        results, _ = self._get("/".join(path), params=params)
        if include_aggregations:
            return CvaClient._results2dict(results)
        else:
            return CvaClient._results2list(results)

    def _render_single_result(self, results, as_data_frame=True):
        first = results[0]
        return self._render(first, as_data_frame)

    @staticmethod
    def _render(results, as_data_frame=True):
        if as_data_frame:
            return json_normalize(results)
        else:
            return results
