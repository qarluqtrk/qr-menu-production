from django.shortcuts import render


def otp_view(request):
    return render(request, 'app/otp.html')
