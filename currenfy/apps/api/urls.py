from django.urls import path
from django.urls import include
from rest_framework import routers
from . import views


router = routers.SimpleRouter()
router.register(r'booked', views.BookedTradesSet, basename='booked')

urlpatterns = [
    path('', include(router.urls)),
    path('fixer/rate', views.rate_without_params, name='fixer-rate'),
    path('fixer/rate/<str:sell_currency>/<str:buy_currency>', views.RateView.as_view(), name='fixer-rate'),
    path('fixer/symbols', views.SymbolsView.as_view(), name='fixer-symbols'),
]
