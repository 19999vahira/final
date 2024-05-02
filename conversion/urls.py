from django.urls import path
from .views import CurrencyConversionAPI

urlpatterns = [
    # URL pattern for currency conversion API
    path('conversion/<str:currency_from>/<str:currency_to>/<str:amount>/', CurrencyConversionAPI.as_view(), name='currency_conversion'),
]



