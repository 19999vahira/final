from django.urls import path
from . import views

app_name = 'financial'

urlpatterns = [
    path('make_payment/', views.make_payment, name='make_payment'),
    path('view_balance/', views.view_balance, name='view_balance'),
    path('view_transactions/', views.view_transactions, name='view_transactions'),
    path('add_money/', views.add_money, name='add_money'),
    path('request_payment/', views.request_payment, name='request_payment'),
    path('view_requests/', views.view_requests, name='view_requests'),
    path('pay_request/<int:request_id>/', views.pay_request, name='pay_request'),
    path('decline_request/<int:request_id>/', views.decline_request, name='decline_request'),
    path('make_payment_request/<str:receiver_username>/<str:amount>/', views.make_payment_request, name='make_payment_request'),
    path('payment_confirmation/', views.payment_confirmation, name='payment_confirmation'),
]
