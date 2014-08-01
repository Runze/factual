"""
Factual API driver
"""

import json
from functools import partial

import requests
from requests_oauthlib import OAuth1

from .query import Resolve, Table, Submit, Insert, Facets, Flag, Geocode, Diffs, Match, Multi, Clear, Boost
from .utils import is_str

API_V3_HOST = "http://api.v3.factual.com"
DRIVER_VERSION_TAG = "factual-python-driver-1.6.0"

class Factual(object):
    def __init__(self, key, secret, timeout=None):
        self.key = key
        self.secret = secret
        self.timeout = timeout
        self.api = API(self._generate_token(key, secret),timeout)

    def table(self, table):
        return Table(self.api, 't/' + table)

    def crosswalk(self):
        return Table(self.api, 't/crosswalk')

    def resolve(self, table, values, debug=False):
        params = {'values': values}
        if debug:
            params['debug'] = 'true'
        return Resolve(self.api, table, params)

    def match(self, table, values):
        return Match(self.api, table, {'values': values})

    def raw_read(self, path, raw_params):
        return self.api.raw_read(path, raw_params)

    def raw_write(self, path, raw_params):
        return self.api.raw_write(path, raw_params)

    def facets(self, table):
        return Facets(self.api, 't/' + table + '/facets')

    def submit(self, table, factual_id=None, values={}):
        return Submit(self.api, table, factual_id, {'values': values})

    def insert(self, table, factual_id=None, values={}):
        return Insert(self.api, table, factual_id, {'values': values})

    def clear(self, table, factual_id, fields):
        return Clear(self.api, table, factual_id, {'fields': fields})

    def flag(self, table, factual_id):
        return Flag(self.api, table, factual_id)

    def boost(self, table, factual_id, q=None):
        return Boost(self.api, table, factual_id, {'factual_id': factual_id, 'q': q})

    def geocode(self, point):
        return Geocode(self.api, 'places/geocode', {'geo': point})

    def diffs(self, table, start, end):
        return Diffs(self.api, 't/' + table + '/diffs', start, end)

    def multi(self, queries):
        return Multi(self.api, queries).make_request()

    def get_row(self, table, factual_id):
        data = self.table(table).factual_id(factual_id).data()
        return data[0]

    def _generate_token(self, key, secret):
        access_token = OAuth1(key, secret)
        return access_token


class API(object):
    def __init__(self, access_token, timeout):
        self.client = requests.Session()
        self.client.auth = access_token
        self.client.timeout = timeout

    def get(self, query):
        response = self._handle_request(query.path, query.params, self._make_get_request)
        return response

    def post(self, query):
        response = self._handle_request(query.path, query.params, self._make_post_request)
        return response
        
    def schema(self, query):
        response = self._handle_request(query.path + '/schema', query.params, self._make_get_request)
        return response['view']

    def raw_read(self, path, raw_params):
        url = self._build_base_url(path)
        return self._make_request(url, raw_params, self._make_get_request).text

    def raw_stream_read(self, path, raw_params):
        url = self._build_base_url(path)
        response = self._make_request(url, raw_params, partial(self._make_get_request, stream=True))
        for line in response.iter_lines(decode_unicode=True):
            if line:
                yield line

    def raw_write(self, path, raw_params):
        url = self._build_base_url(path)
        return self._make_request(url, raw_params, self._make_post_request).text

    def build_url(self, path, params, method):
        return self._prepare_req(path, params, method).url

    def build_multi_url(self, query):
        return self._prepare_req(query.path, query.params, query.method).path_url

    def _prepare_req(self, path, params, method):
        url = self._build_base_url(path)
        req = requests.Request(method, url, params=self._transform_params(params))
        return req.prepare()

    def _build_base_url(self, path):
        return API_V3_HOST + '/' + path

    def _handle_request(self, path, params, request_method):
        url = self._build_base_url(path)
        response = self._make_request(url, params, request_method)
        payload = json.loads(response.text)
        if payload['status'] == 'error':
            raise APIException(response.status_code, payload, response.url)
        return payload['response'] if 'response' in payload else payload

    def _make_request(self, url, params, request_method):
        request_params = self._transform_params(params)
        response = request_method(url, request_params)
        if not 200 <= response.status_code < 300:
            raise APIException(response.status_code, response.text, response.url)
        return response

    def _make_get_request(self, url, params, stream=False):
        headers = {'X-Factual-Lib': DRIVER_VERSION_TAG}
        return self.client.get(url, headers=headers, params=params, timeout=self.client.timeout, stream=stream)

    def _make_post_request(self, url, params):
        headers = {'X-Factual-Lib': DRIVER_VERSION_TAG, 'content-type': 'application/x-www-form-urlencoded'}
        return self.client.post(url, headers=headers, data=params)

    def _transform_params(self, params):
        if is_str(params):
            return params
        string_params = []
        for key, val in params.items():
            transformed = json.dumps(val) if not is_str(val) else val
            string_params.append((key, transformed))
        return dict(string_params)


class APIException(Exception):
    def __init__(self, status_code, response, url):
        self.status_code = status_code
        self.response = response
        self.url = url
        exception = {'http_status_code':status_code,'response':response,'url':url,'driver_version':DRIVER_VERSION_TAG}
        Exception.__init__(self, exception)

    def get_status_code(self):
        return self.status_code

    def get_response(self):
        return self.response
