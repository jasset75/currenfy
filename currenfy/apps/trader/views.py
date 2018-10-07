from django.shortcuts import render


def booked_trades(request):
    return render(request, 'trader/index.html')

def new_trade(request):
    return render(request, 'trader/new_trade.html')