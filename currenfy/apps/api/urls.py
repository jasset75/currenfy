from django.urls import path
from django.urls import include
from rest_framework import routers
from .views import BookedTradesSet
from .views import RateView 


router = routers.SimpleRouter()


#router.register(r'rate', RateView, base_name='rate')

router.register(r'booked', BookedTradesSet)

urlpatterns = [
    path('', include(router.urls)),
    path('fixer/<str:sell_currency>/<str:buy_currency>', RateView.as_view()),
]
