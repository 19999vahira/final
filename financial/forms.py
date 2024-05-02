# financial/forms.py

from django import forms


class PaymentRequestForm(forms.Form):
    recipient_username = forms.CharField(max_length=150, label='Recipient Username')
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label='Amount')

from django import forms

class MoneyForm(forms.Form):
    amount = forms.DecimalField(label='Amount', min_value=0.01, max_digits=10, decimal_places=2)
