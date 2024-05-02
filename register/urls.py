from django.urls import path
from . import views

app_name = 'register'

urlpatterns = [
    path('', views.register_choice, name='register_choice'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
]