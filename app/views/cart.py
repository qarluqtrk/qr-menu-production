from django.http import JsonResponse
from django.shortcuts import render, redirect

from app.utils.cart import Cart
from app.utils.poster import poster


# Actual Cart Page
def cart_view(request):
    cart = Cart(request)
    cart_items = cart.get_cart()
    cart_details = []
    for cart_item in cart_items.copy():
        product = poster.get_product(cart_item)
        if product["sources"][0]['visible'] == 1:
            cart_details.append(
                {
                    "product_id": cart_item,
                    "quantity": cart_items[cart_item]['quantity'],
                    "modification_id": cart_items[cart_item]['modification_id'],
                    "info": product,
                }
            )
        else:
            cart.remove(cart_item)
    cart_total = cart.get_total_price()
    print(cart_details)
    return render(request, 'app/cart.html', {'cart_details': cart_details, 'cart_total': str(cart_total)})


def add_to_cart(request, product_id, modification_id=None):
    cart = Cart(request)
    if modification_id is None:
        cart.add(product_id)
        return redirect('cart')
    else:
        cart.add(product_id, modification_id)
        return redirect('cart')


# Ajax Tools for Cart

def change_quantity(request):
    if request.method == 'POST':
        # getting data from ajax post request
        product_id = request.POST.get('product_id')
        change_method = request.POST.get('change_method')
        # editing cart data
        cart = Cart(request)
        cart.quantity_change(product_id, change_method)
        # cart total
        cart_total = cart.get_total_price()
        # quantity
        quantity = cart.cart[product_id]['quantity']
        return JsonResponse({"status": "success", "cart_total": str(cart_total), "quantity": quantity})


def delete_cart_item(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return JsonResponse({"status": "success", "cart_total": str(cart.get_total_price())})
