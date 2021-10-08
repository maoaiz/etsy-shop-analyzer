from django.contrib import admin

from .models import Item, Shop


class ReadOnly:
    def has_delete_permission(self, request, obj=None):
        return False

    # def has_add_permission(self, request, obj=None):
    #     return False

    def has_change_permission(self, request, obj=None):
        return False


class ItemAdmin(ReadOnly, admin.ModelAdmin):
    list_display = [
        'name',
        'price',
        'currency_code',
        'quantity',
        'num_favorers',
        'shop',
    ]


class ShopAdmin(ReadOnly, admin.ModelAdmin):
    list_display = [
        'shop_id',
        'name',
        'title',
        'url',
    ]


admin.site.register(Item, ItemAdmin)
admin.site.register(Shop, ShopAdmin)
