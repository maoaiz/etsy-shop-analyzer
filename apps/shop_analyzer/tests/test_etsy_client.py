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

        response = self.client._request_all('/some-endpoint')

        response = list(response)

        self.assertEqual(len(response), 0)
