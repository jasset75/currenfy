from django.urls import path
from .views import booked_trades, new_trade

urlpatterns = [
    path('', booked_trades, name='booked_trades_list'),
    path('new_trade', new_trade, name= 'new_trade'),
]
