from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_admin_conf_vars.global_vars import config

from apps.shop_analyzer.models import Shop
from django.core.serializers.json import DjangoJSONEncoder


def home(request):

    shops_qs = Shop.objects.all()
    ignored_terms = config.IGNORED_WORDS

    return render(request, 'shop_analyzer/home.html', locals())


def get_data(request, s_pk):
    '''
    Returns the top N meaningful terms for a shop
    '''

    shop_obj = get_object_or_404(Shop, pk=s_pk)

    limit = request.GET.get('limit', 5)

    terms_data = shop_obj.get_meaningful_terms(limit)

    data = {
        "total_items": shop_obj.get_num_items(),
        "terms": terms_data,
    }

    return JsonResponse(data, encoder=DjangoJSONEncoder, safe=False)
