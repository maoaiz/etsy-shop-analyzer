from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from apps.shop_analyzer.models import Shop
from django.core.serializers.json import DjangoJSONEncoder


def home(request):

    shops_qs = Shop.objects.all()

    return render(request, 'shop_analyzer/home.html', locals())


def get_data(request, s_pk):

    shop_obj = get_object_or_404(Shop, pk=s_pk)

    data = shop_obj.get_items_data()

    return JsonResponse(data, encoder=DjangoJSONEncoder, safe=False)
