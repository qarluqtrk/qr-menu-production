from django.shortcuts import render, redirect

from app.forms import PaymentForm
from app.utils.payment import PaymentProcessor


def payment_view(request):
    if request.method == 'POST':
        print(request.POST)
        form = PaymentForm(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            expiry_date = form.cleaned_data['expiry_date']
            username = 'test_merchant@gmail.com'
            password = 'test_password'
            payment_processor = PaymentProcessor(username, password, card_number, expiry_date)
            payment_processor.get_access_token()
            print(f"AccessToken : {payment_processor.get_access_token()}")
            return redirect('otp')
    form = PaymentForm()
    return render(request, 'app/payment.html', {'form': form})
