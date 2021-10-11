from unittest import TestCase
from unittest.mock import patch

from apps.shop_analyzer.integrations.etsy.client import EtsyClient


class TestEtsyClient(TestCase):
    '''Tests for all methods in EtsyClient class'''

    def setUp(self):
        self.key_string = '123456789acbdefghi'  # fake key string
        self._verbose = False
        self.client = self.__get_client()

    def __get_client(self):
        return EtsyClient(self.key_string, verbose=self._verbose)

    def test_defaults(self):
        '''Verify all params are defined correctly'''

        _base_url = 'https://openapi.etsy.com/v3/application'
        assert self.client.base_url == _base_url
        assert self.client.verbose is False
        assert self.client.key_string == self.key_string

    def test_perform_request_is_called_in_requests_all_method(self):
        self.client

    @patch.object(EtsyClient, 'perform_request')
    def test_request_all_not_returns_offset(self, mock_perform_request):
        """
        Verify when method RestClient.perform_request not returns offset,
        it returns 0 objects
        """

        response = {'count': 0, 'results': []}
        mock_perform_request.return_value = 200, response

        response = self.client._request_all('/some-endpoint', limit=10, offset=0)

        response = list(response)

        self.assertEqual(len(response), 0)

    @patch.object(EtsyClient, 'perform_request')
    def test_request_all_calls_perform_request(self, mock_perform_request):
        '''Verify if the method RestClient.perform_request is called'''

        response = {'count': 2, 'results': [{}, {}]}
        mock_perform_request.return_value = 200, response

        params = {'limit': 10, 'offset': 0}

        response = self.client._request_all('/some-endpoint', **params)

        # using generator
        list(response)

        mock_perform_request.assert_called_once()
        mock_perform_request.assert_called_with('/some-endpoint', params=params)

    @patch.object(EtsyClient, 'perform_request')
    def test_request_all_calls_perform_request_n_times(self, mock_perform_request):
        '''Verify if the method RestClient.perform_request is called'''

        response = {'count': 5, 'results': [{}, {}]}
        params = {'limit': 2, 'offset': 0}

        mock_perform_request.return_value = 200, response

        response = self.client._request_all('/some-endpoint', **params)

        # using generator
        list(response)

        calls = mock_perform_request.call_count

        # 6 request have to exist with the next objects:
        # 1. 1 and 2,
        # 2. 3 and 4,
        # 3. 5 (the last)
        self.assertEqual(calls, 3)

    @patch.object(EtsyClient, '_request_all')
    def test_get_shops_by_name(self, mock_request_all):

        shop_name = 'my-shop'
        _ = self.client.get_shops_by_name(shop_name)

        mock_request_all.assert_called_once()
        mock_request_all.assert_called_with(f'/shops?shop_name={shop_name}')
