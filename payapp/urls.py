# payapp/urls.py

from django.urls import path
from . import views

app_name = 'payapp'

urlpatterns = [
    path('', views.payapp_home, name='payapp_home'),
    path('logout/', views.logout_view, name='logout_view'),  # URL pattern for logout_view
]

