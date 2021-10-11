from unittest import TestCase

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
