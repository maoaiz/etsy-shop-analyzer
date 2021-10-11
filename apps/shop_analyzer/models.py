from django.db import models


class Shop(models.Model):
    shop_id = models.IntegerField(db_index=True)
    name = models.CharField(max_length=256)
    title = models.TextField(null=True, blank=True)
    url = models.URLField(max_length=400)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or f'<No name> id={self.id}'

    def get_num_items(self):
        return self.item_set.all().count()

    def get_items_data(self, ordered_by='num_favorers', order_type="desc", limit=5):
        ot = '-' if order_type == 'desc' else ''
        qs = self.item_set.all().order_by(f'{ot}{ordered_by}')[:int(limit)]
        return [q.get_data() for q in qs]

    def get_meaningful_terms(self):
        pass

    @staticmethod
    def get_shops_by_ids(shop_ids):
        '''
        Returns a Shop queryset for shop_ids.
        Parameters:
        -----------
        shop_ids: list
            The list of shop ids to check
        '''
        return Shop.objects.filter(shop_id__in=shop_ids)

    @staticmethod
    def get_unsynced_shop_ids(shop_ids):
        '''
        Returs a list of shop ids that are not already synced to the database.
        Parameters:
        -----------
        shop_ids: list
            The list of shop ids to check
        '''
        shop_ids = set(shop_ids)

        qs = Shop.objects.filter(shop_id__in=shop_ids)

        already_synced_shops = list(qs.values_list('shop_id', flat=True))

        shop_ids.difference_update(set(already_synced_shops))

        return list(shop_ids)

class Item(models.Model):

    shop = models.ForeignKey('Shop', on_delete=models.PROTECT)
    item_id = models.IntegerField(db_index=True)  # to store 'listing_id'. Etsy calls listing to items
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=6, max_digits=32)
    currency_code = models.CharField(max_length=5)
    quantity = models.IntegerField()
    num_favorers = models.IntegerField()
    url = models.URLField(max_length=400, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or f'<No name> id={self.id}'

    def get_data(self):
        return {
            'item_id': self.item_id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'currency_code': self.currency_code,
            'quantity': self.quantity,
            'num_favorers': self.num_favorers,
            'url': self.url,
        }
