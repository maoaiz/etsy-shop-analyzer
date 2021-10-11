from unittest import TestCase
import pytest_httpbin
from apps.shop_analyzer.integrations.rest_client import RestClient
import os


@pytest_httpbin.use_class_based_httpbin
class TestRestClient(TestCase):

    def test_defaults(self):
        '''Checking RestClient attributes matches'''

        rest_client = RestClient('https://example.com')
        assert rest_client.base_url == 'https://example.com'
        assert rest_client.verbose is False

    def test_verbose_param_in_true(self):
        rest_client = RestClient('https://example.com', verbose=True)
        assert rest_client.verbose is True

    def test_verbose_param_in_false(self):
        rest_client = RestClient('https://example.com', verbose=False)
        assert rest_client.verbose is False

    def test_perform_get_request(self):
        rest_client = RestClient(self.httpbin.url)
        status, data = rest_client.perform_request('/get', {}, 'GET')
        assert status == 200
        assert data['args'] == {}
        assert 'headers' in data

    def test_perform_get_request_with_params(self):
        rest_client = RestClient(self.httpbin.url)
        params = {'arg1': '3', 'arg2': '4'}
        status, data = rest_client.perform_request('/get', params=params, method='GET')
        assert status == 200
        assert data['args'] == params
        assert data['headers']['Content-Type'] == 'application/json'
