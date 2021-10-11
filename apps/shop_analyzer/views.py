from django.shortcuts import render

from apps.shop_analyzer.models import Shop


def home(request):

    shops_qs = Shop.objects.all()

    return render(request, 'shop_analyzer/home.html', locals())
