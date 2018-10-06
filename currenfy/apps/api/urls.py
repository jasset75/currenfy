from django.urls import path
from django.urls import include
from rest_framework import routers
from .views import BookedTradesSet
from .views import RateView, SymbolsView 


router = routers.SimpleRouter()
router.register(r'booked', BookedTradesSet, base_name='booked')

urlpatterns = [
    path('', include(router.urls)),
    path('fixer/rate/<str:sell_currency>/<str:buy_currency>', RateView.as_view(), name='fixer-rate'),
    path('fixer/symbols', SymbolsView.as_view(), name='fixer-symbols'),
]
