import time

from django.http import JsonResponse
from django.shortcuts import render, redirect

from app.utils.cart import Cart
from app.utils.poster import poster


# Actual Cart Page
def cart_view(request):
    start_time = time.time()
    cart = Cart(request)
    cart_items = cart.get_cart()

    poster_products = poster.get_products()
    poster_products_dict = {}
    for i in poster_products:
        poster_products_dict[i["product_id"]] = i

    cart_details = []
    if request.session['cart']:
        try:
            for cart_item in cart_items.copy():
                product = poster_products_dict[cart_item]

                if "modifications" in product:
                    for modification in product["modifications"]:
                        if int(modification["modificator_id"]) == int(cart_items[cart_item]["modification_id"]):
                            if isinstance(product["sources"], list) and product["sources"]:
                                if modification["sources"][0]["visible"] == True:
                                    cart_details.append(
                                        {
                                            "product_id": cart_item,
                                            "quantity": cart_items[cart_item]["quantity"],
                                            "modification_id": str(cart_items[cart_item]["modification_id"]),
                                            "info": product,
                                        }
                                    )
                                    break
                                else:
                                    cart.remove(cart_item)
                                    break
                else:
                    if product["sources"][0]["visible"] == True:
                        if "group_modifications" in product:
                            cart_details.append(
                                {
                                    "product_id": cart_item,
                                    "quantity": cart_items[cart_item]["quantity"],
                                    "modification_id": int(cart_items[cart_item]["modification_id"]),
                                    "info": product,
                                }
                            )
                        else:
                            cart_details.append(
                                {
                                    "product_id": cart_item,
                                    "quantity": cart_items[cart_item]["quantity"],
                                    "modification_id": str(cart_items[cart_item]["modification_id"]),
                                    "info": product,
                                }
                            )
                    else:
                        cart.remove(cart_item)

        except:
            request.session['cart'] = {}
            return redirect('cart')

        cart_total = cart.get_total_price()

        return render(request, 'app/cart.html', {'cart_details': cart_details, 'cart_total': str(cart_total)})
    else:
        return redirect('empty-cart')


def add_to_cart(request, product_id, modification_id=None):
    cart = Cart(request)
    if modification_id is None:
        cart.add(product_id)
        return redirect('cart')
    else:
        cart.add(product_id, modification_id)
        return redirect('cart')


def add_to_cart_post(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        modification_id = request.POST.get('modification_id')
        cart = Cart(request)
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
    data = {"status": "success", "cart_total": str(cart.get_total_price())}
    return JsonResponse(data, safe=False)


def make_order(request):
    cart = Cart(request)
    cart_items = cart.get_cart()

    products = []
    for cart_item in cart_items:
        if cart_items[f"{cart_item}"]['modification_id'] == 0:
            products.append({"product_id": cart_item, "count": cart_items[cart_item]['quantity']})
        else:
            products.append({"product_id": cart_item,
                             "modification": [{"m": str(cart_items[f"{cart_item}"]["modification_id"]), "a": 1}, ],
                             "count": cart_items[cart_item]['quantity']})
    table_id = request.session.get('table_id')
    if not table_id:
        return JsonResponse({"status": "error", "message": "'table_id' not found in session"})

    else:

        poster.create_dine_in_order(products, table_id=request.session['table_id'])
        # cart clear
        request.session['cart'] = {}
        return JsonResponse({"status": "success"})


def empty_cart_view(request):
    return render(request, 'app/empty-cart.html')
