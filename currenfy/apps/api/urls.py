from django.urls import path
from django.urls import include
from rest_framework import routers
from .views import BookedTradesSet


router = routers.DefaultRouter()
router.register(r'booked', BookedTradesSet)

urlpatterns = [
    path('', include(router.urls)),
]
