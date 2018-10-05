from django.urls import path
from django.urls import include
from rest_framework import routers
from .views import BookedTradesSet
from .views import get_rate 


router = routers.DefaultRouter()
router.register(r'booked', BookedTradesSet)

urlpatterns = [
    path('', include(router.urls)),
    path('rate',  get_rate)
]
