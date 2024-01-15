from django.http import JsonResponse
from django.shortcuts import render, redirect

from app.forms import PaymentForm
from app.utils.cart import Cart
from app.utils.payment import PaymentProcessor


def payment_view(request):
    cart = Cart(request)
    cart_total = cart.get_total_price()
    if request.method == 'POST' and 'application/json' in request.headers.get('Accept', ''):
        form = PaymentForm(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data['card_number'].replace(" ", "")
            expiry_date = form.cleaned_data['expiry_date'].replace("/", "")
            print(f"{card_number} {expiry_date}")
            payment_processor = PaymentProcessor(card_number, expiry_date, cart_total)
            global payment_obj
            payment_obj = payment_processor
            print(f"AccessToken : {payment_processor.auth_token}")
            print(f"phone: {payment_processor.phone_number}")
            print(f"Cart total: {payment_processor.cart_total}")
            return JsonResponse({"success": True, "phone": payment_processor.phone_number})

        else:
            return JsonResponse({"success": False})
    elif request.POST.get('step') == '2':
        print('step 2')
        payment_obj.confirm_card(otp=request.POST.get('otp'))
        return redirect('index')
    form = PaymentForm()
    return render(request, 'app/payment.html', {'form': form})
