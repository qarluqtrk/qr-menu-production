from django.shortcuts import render

from app.utils.poster import poster


def products_view(request, category_id):
    products = poster.get_products(category_id)
    return render(request, 'app/products.html',
                  {'products': products})
