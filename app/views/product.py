from django.http import JsonResponse
from django.shortcuts import render

from app.utils.poster import poster


def product_view(request, product_id):
    product = poster.get_product(product_id)
    similar_products = poster.get_products(category_id=int(product['menu_category_id']))
    return render(request, 'app/product.html',
                  {'product': product, 'similar_products': similar_products[:5]})


def product_info_json(request, product_id):
    product = poster.get_product(product_id)
    return JsonResponse({'product': product})
