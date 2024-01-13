from django.http import JsonResponse
from django.shortcuts import render
from urllib3 import HTTPResponse

from app.forms import PaymentForm
from app.utils.payment import PaymentProcessor


def payment_view(request):
    if request.method == 'POST' and 'application/json' in request.headers.get('Accept', ''):
        print(request.POST)
        form = PaymentForm(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data['card_number'].replace(" ", "")
            expiry_date = form.cleaned_data['expiry_date'].replace("/", "")
            print(f"{card_number} {expiry_date}")
            payment_processor = PaymentProcessor(card_number, expiry_date)
            print(f"AccessToken : {payment_processor.auth_token}")
            print(f"phone: {payment_processor.phone_number}")
            return JsonResponse({"success": True, "phone": payment_processor.phone_number})
    form = PaymentForm()
    return render(request, 'app/payment.html', {'form': form})
