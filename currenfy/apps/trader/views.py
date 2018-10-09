from django.shortcuts import render
from django.conf import settings


def booked_trades(request):
    return render(request, 'trader/index.html')


def new_trade(request):
    return render(request, 'trader/new_trade.html')


def currenfy_js(request):
    return render(request, 'trader/js/currenfy.js', {'rate_precision': settings.RATE_DECIMAL_PRECISION})
