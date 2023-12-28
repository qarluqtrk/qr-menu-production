from django.shortcuts import render, redirect

from app.utils.cart import Cart
from app.utils.poster import poster


def cart_view(request):
    cart = Cart(request)
    cart_items = cart.get_cart()
    cart_details = []
    for cart_item in cart_items:
        cart_details.append(
            {
                "product_id": cart_item,
                "quantity": cart_items[cart_item]['quantity'],
                "modification_id": cart_items[cart_item]['modification_id'],
                "info": poster.get_product(cart_item),
            }
        )
    cart_total = cart.get_total_price()
    print(cart_details)
    return render(request, 'app/cart.html', {'cart_details': cart_details, 'cart_total': str(cart_total)})


def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return redirect('cart')
