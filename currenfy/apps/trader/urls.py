from django.urls import path
from .views import booked_trades, new_trade, currenfy_js

urlpatterns = [
    path('', booked_trades, name='booked_trades_list'),
    path('js/currenfy.js', currenfy_js, name='currenfy_js'),
    path('new_trade', new_trade, name='new_trade'),
]
