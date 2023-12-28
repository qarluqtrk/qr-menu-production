from django.urls import path

from app.views.cart import cart_view, add_to_cart
from app.views.index import index_view
from app.views.product import product_view, product_info_json
from app.views.products import products_view

urlpatterns = [
    path('', index_view, name='index'),
    path('products/<int:category_id>/', products_view, name='products'),
    path('product/<int:product_id>/', product_view, name='product'),

    # AJAX
    path('product-json/<int:product_id>/', product_info_json, name='product-json'),


    # cart
    path('cart/', cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add-to-cart'),
]