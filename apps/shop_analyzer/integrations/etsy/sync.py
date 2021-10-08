import logging

from django.conf import settings
from django.db import transaction
from apps.shop_analyzer.models import Shop

from .client import EtsyClient

logger = logging.getLogger(__name__)


class EtsySync:
    """
    Contains the logic to sync Etsy with the DB
    Parameters:
    -----------
    key_string : str
        Etsy key string.
    """

    def __init__(self, key_string=settings.ETSY_KEYSTRING, verbose=False):
        self.verbose = verbose
        self._client = EtsyClient(key_string, verbose=verbose)

    def sync_shops(self, shop_names):
        """
        Sync Etsy shops to the database based on a list of shop names.
        Parameters:
        -----------
        shop_names : list
            A list with the shop names to sync
        """

        if not isinstance(shop_names, list):
            raise ValueError("Please define a python list for shp_names")

        with transaction.atomic():

            # Sync only new shops
            shop_names_to_sync = Shop.get_unsynced_shop_names(shop_names)

            data = []

            for shop_name in shop_names_to_sync:

                shops = self._client.get_shops_by_name(shop_name)

                for shop in shops:
                    new_shop = Shop(
                        shop_id=shop.get('shop_id'),
                        name=shop.get('shop_name', shop_name),
                        title=shop.get('title', '--'),
                        url=shop.get('url', ''),
                    )
                    data.append(new_shop)

            Shop.objects.bulk_create(data)

        output = f'{len(data)} shops were synced'
        logger.info(output)
        return output

    def sync(self, shop_names=settings.ETSY_SHOP_NAMES):
        """
        Syncs the data from Etsy to the DB
        """

        self.sync_shops(shop_names)
