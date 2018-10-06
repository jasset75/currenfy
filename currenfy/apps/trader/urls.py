from django.urls import path
from .views import trader

urlpatterns = [
    path('', trader),
]
