import logging

from django.conf import settings
from django.db import transaction
from apps.shop_analyzer.models import Item, Shop

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

    def sync_shops(self, shop_ids):
        """
        Sync Etsy shops to the database based on a list of shop names.
        Parameters:
        -----------
        shop_ids : list
            A list with the shop ids to sync
        """

        if not isinstance(shop_ids, list):
            raise ValueError("Please define a python list for shop_ids")

        with transaction.atomic():

            # Sync only new shops
            self.new_shop_ids = Shop.get_unsynced_shop_ids(shop_ids)

            data = []

            for shop_id in self.new_shop_ids:

                shop = self._client.get_shop_by_id(shop_id)
                new_shop_obj = Shop(
                    shop_id=shop.get('shop_id'),
                    name=shop.get('shop_name'),
                    title=shop.get('title', '--'),
                    url=shop.get('url', ''),
                )
                data.append(new_shop_obj)

            Shop.objects.bulk_create(data)

        output = f'{len(data)} shops were synced'
        logger.info(output)
        return output

    def sync_items_for_new_shops(self):
        '''
        Syncs the items for the new shops to the DB.
        '''

        with transaction.atomic():

            # get the objects to make the relation with the new Items
            shops_qs = Shop.get_shops_by_ids(self.new_shop_ids)

            for shop_obj in shops_qs:

                data = []

                # get the shop data from the API
                items = self._client.get_items_by_shop(shop_obj.shop_id)

                for item in items:
                    # parse data to store in the Item model

                    price_data = item.get('price', {})
                    try:
                        price = price_data.get('amount', 0) / price_data.get('divisor', 100)
                    except Exception:
                        price = 0

                    currency_code = price_data.get('currency_code')

                    item_obj = Item(
                        shop=shop_obj,
                        item_id=item.get('listing_id'),
                        name=item.get('title'),
                        description=item.get('description'),
                        price=price,
                        currency_code=currency_code,
                        quantity=item.get('quantity'),
                        num_favorers=item.get('num_favorers'),
                        url=item.get('url'),
                    )
                    data.append(item_obj)

                Item.objects.bulk_create(data)

    def sync(self, shop_ids=settings.ETSY_SHOP_IDS):
        """
        Syncs the data from Etsy to the DB
        """

        self.sync_shops(shop_ids)

        self.sync_items_for_new_shops()
