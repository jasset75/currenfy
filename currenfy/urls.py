from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('', include('trader.urls')),   # home app: trader
    path('api/', include('api.urls')),  # api interface
    path('admin/', admin.site.urls),    # admin
]
