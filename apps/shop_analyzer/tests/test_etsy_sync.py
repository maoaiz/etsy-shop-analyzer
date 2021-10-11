from unittest import TestCase
from unittest.mock import patch

from apps.shop_analyzer.integrations.etsy.client import EtsyClient
from apps.shop_analyzer.integrations.etsy.sync import EtsySync


class TestEtsyClient(TestCase):
    '''Tests for all methods in EtsyClient class'''

    def setUp(self):
        self.key_string = '123456789acbdefghi'  # fake key string
        self._verbose = False
        self.sync = EtsySync(self.key_string, verbose=self._verbose)

    def test_defaults(self):
        '''Verify all params are defined correctly'''

        self.assertIsInstance(self.sync._client, EtsyClient)

    @patch.object(EtsySync, 'sync_shops')
    @patch.object(EtsySync, 'sync_items_for_new_shops')
    def test_sync_methods_are_called_called(self, mock_sync_items_for_new_shops, mock_sync_shops):
        '''
        EtsySync.sync must call two methods:
            EtsySync.sync_shops
            EtsySync.sync_items_for_new_shops
        '''

        self.sync.sync()

        mock_sync_shops.assert_called_once()
        mock_sync_items_for_new_shops.assert_called_once()

    @patch.object(EtsySync, 'sync_shops')
    @patch.object(EtsySync, 'sync_items_for_new_shops')
    def test_sync_shops_called_with(self, mock_sync_items_for_new_shops, mock_sync_shops):

        ids = [1, 2, 3]

        self.sync.sync(shop_ids=ids)

        mock_sync_shops.assert_called_with(ids)
