# register/models.py

from django.contrib.auth.models import User
from django.db import models

class Account(models.Model):
    CURRENCY_CHOICES = [
        ('GBP', 'GBP'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='GBP')

    def __str__(self):
        return f"{self.user.username}'s account"


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('DEPOSIT', 'Deposit'),
        ('TRANSFER', 'Transfer'),
    ]

    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE, null=True, blank=True)
    receiver = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)


class PaymentRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_payment_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_payment_requests', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending')
    declined = models.BooleanField(default=False)  # New field to track if the request has been declined

    def __str__(self):
        return f"Payment Request from {self.sender.username} to {self.receiver.username} - {self.amount}"