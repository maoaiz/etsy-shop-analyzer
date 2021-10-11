from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from apps.shop_analyzer.models import Shop
from django.core.serializers.json import DjangoJSONEncoder


def home(request):

    shops_qs = Shop.objects.all()
    orders = [
        'price',
        'quantity',
        'num_favorers',
    ]

    return render(request, 'shop_analyzer/home.html', locals())


def get_data(request, s_pk):
    '''
    Returns the top five items ordered by some field
    '''
    shop_obj = get_object_or_404(Shop, pk=s_pk)

    order_by = request.GET.get('order_by', 'num_favorers')
    order_type = request.GET.get('order_type', 'desc')
    limit = request.GET.get('limit', 5)

    top_data = shop_obj.get_items_data(
        ordered_by=order_by, order_type=order_type, limit=limit
    )

    data = {
        "total_items": shop_obj.get_num_items(),
        "top_data": top_data,
    }

    return JsonResponse(data, encoder=DjangoJSONEncoder, safe=False)
