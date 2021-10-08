from django.db import models


class Shop(models.Model):
    shop_id = models.IntegerField(db_index=True)
    name = models.CharField(max_length=256)
    title = models.TextField()
    url = models.URLField(max_length=400)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or f'<No name> id={self.id}'

class Item(models.Model):

    shop = models.ForeignKey('Shop', on_delete=models.PROTECT)
    item_id = models.IntegerField(db_index=True)  # to store 'listing_id'. Etsy calls listing to items
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=6, max_digits=32)
    currency_code = models.CharField(max_length=5)
    quantity = models.IntegerField()
    num_favorers = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or f'<No name> id={self.id}'
