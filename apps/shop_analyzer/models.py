import re
import operator
from django.db import models

from django_admin_conf_vars.global_vars import config


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

    def get_meaningful_terms(self, limit):
        '''
        Returns a list with the 'limit' meaningful terms for this shop

        Parameters:
        -----------
        limit: int
            The number of terms to return
        '''

        limit = int(limit)

        ignored_terms = config.IGNORED_WORDS

        pattern = re.compile(f"\\b({ignored_terms})\\W", re.I)

        items = self.item_set.all()

        data = {}

        for item in items:
            word = f"{item.name} {item.description}"

            # remove special characters
            word = word.replace(',', '').replace('-', '')

            # remove ignored words
            word = pattern.sub("", word.lower())

            terms = word.split(' ')

            # count the number of occurencies
            for t in terms:
                if t not in data:
                    data[t] = 1
                else:
                    data[t] += 1

        sorted_data = sorted(data.items(), key=operator.itemgetter(1), reverse=True)

        return {'titles': ['Term', 'Count'], 'data': list(sorted_data[:limit])}

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
    price = models.DecimalField(decimal_places=6, max_digits=32, null=True, blank=True)
    currency_code = models.CharField(max_length=5, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    num_favorers = models.IntegerField(null=True, blank=True)
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
