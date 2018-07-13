import logging
import requests
import datetime
import json
import abc
from furl import furl
import pyark.backoff_retrier as backoff_retrier
from pyark.errors import CvaServerError, CvaClientError


class RestClient(object):

    session = requests.Session()

    def __init__(self, url_base, endpoint_base=None, retries=5):
        self.url_base = url_base
        self.endpoint_base = endpoint_base
        self.headers = {
            'Accept': 'application/json'
        }
        self.token = None
        self.renewed_token = False
        # decorates the REST verbs with retries
        self.get = backoff_retrier.wrapper(self.get, retries)
        self.post = backoff_retrier.wrapper(self.post, retries)
        self.delete = backoff_retrier.wrapper(self.delete, retries)

    def build_url(self, endpoint):
        f = furl(self.url_base)
        segments = []
        if self.endpoint_base:
            segments = self.endpoint_base.split("/")
        endpoint = endpoint.split("/")
        if isinstance(endpoint, (list,)):
            segments = segments + endpoint
        else:
            segments.append(endpoint)
        f.path.segments = segments
        return f.url

    def set_authenticated_header(self, renew_token=False):
        if not self.token or renew_token:
            self.token = self.get_token()
        self.headers["Authorization"] = "{token}".format(token=self.token)

    @abc.abstractmethod
    def get_token(self):
        raise ValueError("Not implemented")

    def post(self, endpoint, payload, params={}, session=True):
        if endpoint is None or payload is None:
            raise ValueError("Must define payload and endpoint before post")
        url = self.build_url(endpoint)
        logging.info("{date} {method} {url}".format(
            date=datetime.datetime.now(),
            method="POST",
            url="{}?{}".format(url, "&".join(RestClient._build_parameters(params)))
        ))
        if session:
            response = self.session.post(url, json=payload, params=params, headers=self.headers)
        else:
            response = requests.post(url, json=payload, params=params, headers=self.headers)
        self._verify_response(response)
        return response.json(), dict(response.headers)

    def get(self, endpoint, params={}, session=True):
        if endpoint is None:
            raise ValueError("Must define endpoint before get")
        url = self.build_url(endpoint)
        logging.info("{date} {method} {url}".format(
            date=datetime.datetime.now(),
            method="GET",
            url="{}?{}".format(url, "&".join(RestClient._build_parameters(params)))
        ))
        if session:
            response = self.session.get(url, params=params, headers=self.headers)
        else:
            response = requests.get(url, params=params, headers=self.headers)
        self._verify_response(response)
        return response.json(), dict(response.headers)

    def patch(self, endpoint, params={}, session=True):
        if endpoint is None:
            raise ValueError("Must define endpoint before patch")
        url = self.build_url(endpoint)
        logging.info("{date} {method} {url}".format(
            date=datetime.datetime.now(),
            method="PATCH",
            url="{}?{}".format(url, "&".join(RestClient._build_parameters(params)))
        ))
        if session:
            response = self.session.patch(url, params=params, headers=self.headers)
        else:
            response = requests.patch(url, params=params, headers=self.headers)
        self._verify_response(response)
        return response.json(), dict(response.headers)

    def delete(self, endpoint, params={}):
        if endpoint is None:
            raise ValueError("Must define endpoint before get")
        url = self.build_url(endpoint)
        logging.info("{date} {method} {url}".format(
            date=datetime.datetime.now(),
            method="DELETE",
            url="{}?{}".format(url, "&".join(RestClient._build_parameters(params)))
        ))
        response = self.session.delete(url, params=params)
        self._verify_response(response)
        return response.json(), dict(response.headers)

    @staticmethod
    def _build_parameters(params):
        parsed_params = []
        for k, v in params.iteritems():
            if isinstance(v, list):
                parsed_params.extend(["{}={}".format(k, e) for e in v])
            else:
                parsed_params.append("{}={}".format(k, v))
        return parsed_params

    def _verify_response(self, response):
        logging.debug("{date} response status code {status}".format(
            date=datetime.datetime.now(),
            status=response.status_code)
        )
        if response.status_code != 200:
            logging.error(response.content)
            # first 403 renews the token, second 403 in a row fails
            if response.status_code == 403 and not self.renewed_token:
                # renews the token if unauthorised
                self.set_authenticated_header(renew_token=True)
                self.renewed_token = True
                # RequestException will trigger a retry and with the renewed token it may work
                raise requests.exceptions.RequestException(response=response)
            # ValueError will not
            if 500 <= response.status_code < 600:
                raise CvaServerError("{}:{}".format(response.status_code, response.text))
            elif 400 <= response.status_code < 500:
                raise CvaClientError("{}:{}".format(response.status_code, response.text))
            else:
                raise ValueError("{}:{}".format(response.status_code, response.text))
        else:
            # once a 200 response token is not anymore just renewed, it can be renewed again if a 403 arrives
            self.renewed_token = False
