from django.urls import path

from app.views.cart import cart_view, add_to_cart, change_quantity, delete_cart_item, add_to_cart_post, make_order
from app.views.index import index_view
from app.views.product import product_view, product_info_json
from app.views.products import products_view
from app.views.table_manager import table_manager

urlpatterns = [
    path('', index_view, name='index'),
    path('products/<int:category_id>/', products_view, name='products'),
    path('product/<int:product_id>/', product_view, name='product'),

    # AJAX
    path('product-json/<int:product_id>/', product_info_json, name='product-json'),
    path('change-quantity/', change_quantity, name='change-quantity'),
    path('delete-cart-item/<int:product_id>/', delete_cart_item, name='delete-cart-item'),

    # cart
    path('cart/', cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('add-to-cart-post/', add_to_cart_post, name='add-to-cart-post'),
    path('make-order/', make_order, name='make-order'),
    path('table_manager/<int:table_id>/', table_manager, name='table_manager'),
]
