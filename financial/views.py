from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from register.models import Account, Transaction, PaymentRequest
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils import timezone
#from thrift_final.client import get_timestamp
from django.contrib import messages
from django.db import transaction
import random
import string

@login_required
def make_payment(request):
    if request.method == 'POST':
        receiver_username = request.POST.get('receiver_username')
        amount = Decimal(request.POST.get('amount', '0'))

        try:
            with transaction.atomic():
                sender_account, _ = Account.objects.get_or_create(user=request.user)
                receiver = User.objects.get(username=receiver_username)
                receiver_account, _ = Account.objects.get_or_create(user=receiver)

                if sender_account.currency != receiver_account.currency:
                    # Perform currency conversion here
                    # For demonstration, assuming 1:1 conversion
                    converted_amount = amount
                else:
                    converted_amount = amount

                if sender_account.balance >= amount and amount > 0:
                    sender_account.balance -= amount
                    receiver_account.balance += converted_amount
                    sender_account.save()
                    receiver_account.save()

                    # Call the function to get the current timestamp
                    timestamp = timezone.now()

                    Transaction.objects.create(sender=request.user, receiver=receiver, amount=amount, timestamp=timestamp)

                    messages.success(request, 'Payment successful!')
                elif amount <= 0:
                    messages.error(request, 'Invalid amount.')
                else:
                    messages.error(request, 'Insufficient funds.')

        except User.DoesNotExist:
            messages.error(request, 'Receiver does not exist.')

    return render(request, 'financial/make_payment.html')  # Render the payment page



@login_required
def view_balance(request):
    account, _ = Account.objects.get_or_create(user=request.user)
    currency_code = account.currency
    balance = account.balance
    currency_symbols = {'USD': '$', 'EUR': '€', 'GBP': '£'}  # Add more currencies if needed
    currency_symbol = currency_symbols.get(currency_code, '')

    return render(request, 'financial/view_balance.html', {'currency_symbol': currency_symbol, 'balance': balance})


@login_required
def view_transactions(request):
    user = request.user
    sent_transactions = Transaction.objects.filter(sender=user)
    received_transactions = Transaction.objects.filter(receiver=user)
    added_money_transactions = Transaction.objects.filter(receiver=user).exclude(sender=user)
    return render(request, 'financial/transactions.html',
                  {'sent_transactions': sent_transactions, 'received_transactions': received_transactions, 'added_money_transactions': added_money_transactions})

@login_required
def add_money(request):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount', '0'))
        captcha_input = request.POST.get('captcha_input', '')

        # Retrieve the generated random string from the form data
        random_string = request.POST.get('random_string', '')

        # Validate the input
        if captcha_input == random_string:
            try:
                with transaction.atomic():
                    if amount > 0:
                        account, _ = Account.objects.get_or_create(user=request.user)
                        account.balance += amount
                        account.save()

                        timestamp = timezone.now()
                        Transaction.objects.create(receiver=request.user, amount=amount, timestamp=timestamp, transaction_type='DEPOSIT')

                        messages.success(request, 'Money added successfully!')
                    else:
                        messages.error(request, 'Invalid amount.')
            except ValueError:
                messages.error(request, 'Invalid amount.')
        else:
            messages.error(request, 'Incorrect characters. Please try again.')

    # Generate random string for CAPTCHA
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    return render(request, 'financial/add_money.html', {'random_string': random_string})

@login_required
def request_payment(request):
    if request.method == 'POST':
        sender_username = request.POST.get('sender_username')
        receiver_username = request.POST.get('receiver_username')
        amount = Decimal(request.POST.get('amount', '0'))

        try:
            with transaction.atomic():
                # Checking if the sender and receiver usernames are correct
                if sender_username != request.user.username:
                    messages.error(request, 'Please enter your username correctly.')
                elif sender_username == receiver_username:
                    messages.error(request, 'Sender and receiver usernames cannot be the same.')
                elif not User.objects.filter(username=receiver_username).exists():
                    messages.error(request, 'Receiver does not exist.')
                else:
                    sender_account, _ = Account.objects.get_or_create(user=request.user)
                    receiver = User.objects.get(username=receiver_username)
                    receiver_account, _ = Account.objects.get_or_create(user=receiver)

                    # Create a payment request
                    PaymentRequest.objects.create(sender=request.user, receiver=receiver, amount=amount)

                    messages.success(request, 'Payment request sent successfully!')
        except ValueError:
            messages.error(request, 'Invalid amount.')

    return render(request, 'financial/request_payment.html')

@login_required
def view_requests(request):
    if request.method == 'POST':
        if 'pay_request' in request.POST:
            request_id = request.POST.get('pay_request')
            # Redirect to the make_payment_request view with the request_id parameter
            return redirect('financial:make_payment_request', request_id=request_id)

    received_pending_requests = PaymentRequest.objects.filter(receiver=request.user, status='pending')
    received_accepted_requests = PaymentRequest.objects.filter(receiver=request.user, status='accepted')
    received_declined_requests = PaymentRequest.objects.filter(receiver=request.user, status='declined')
    sent_requests = PaymentRequest.objects.filter(sender=request.user)

    account, _ = Account.objects.get_or_create(user=request.user)
    currency_code = account.currency
    currency_symbols = {'USD': '$', 'EUR': '€', 'GBP': '£'}  # Add more currencies if needed
    currency_symbol = currency_symbols.get(currency_code, '')

    return render(request, 'financial/view_requests.html', {
        'currency_symbol': currency_symbol,
        'received_pending_requests': received_pending_requests,
        'received_accepted_requests': received_accepted_requests,
        'received_declined_requests': received_declined_requests,
        'sent_requests': sent_requests
    })

@login_required
def decline_request(request, request_id):
    try:
        payment_request = PaymentRequest.objects.get(pk=request_id)
        payment_request.status = 'declined'
        payment_request.save()
        messages.success(request, 'Payment request declined successfully!')
    except PaymentRequest.DoesNotExist:
        messages.error(request, 'Payment request does not exist.')
    return redirect('financial:view_requests')


@login_required
def make_payment_request(request, receiver_username, amount):
    if request.method == 'POST':
        try:
            amount = Decimal(amount)

            sender_account, _ = Account.objects.get_or_create(user=request.user)
            receiver = User.objects.get(username=receiver_username)
            receiver_account, _ = Account.objects.get_or_create(user=receiver)

            if sender_account.currency != receiver_account.currency:
                # Perform currency conversion here
                # For demonstration, assuming 1:1 conversion
                converted_amount = amount  # Replace with your conversion logic
            else:
                converted_amount = amount

            if sender_account.balance >= amount and amount > 0:
                sender_account.balance -= amount
                receiver_account.balance += converted_amount
                sender_account.save()
                receiver_account.save()

                timestamp = timezone.now()
                transaction = Transaction.objects.create(sender=request.user, receiver=receiver, amount=amount, timestamp=timestamp)

                # Delete the payment request
                payment_request = PaymentRequest.objects.filter(sender=request.user, receiver=receiver, amount=amount).first()
                if payment_request:
                    payment_request.delete()

                messages.success(request, 'Payment request sent successfully!')
                # Redirect to payment confirmation page
                return redirect('financial:payment_confirmation')
            elif amount <= 0:
                messages.error(request, 'Invalid amount.')
            else:
                messages.error(request, 'Insufficient funds.')

        except User.DoesNotExist:
            messages.error(request, 'Receiver does not exist.')

    return render(request, 'financial/make_payment_request.html', {'receiver_username': receiver_username, 'amount': amount})

@login_required
def payment_confirmation(request):
    # Remove the payment request from view after payment confirmation
    payment_request_id = request.session.pop('payment_request_id', None)
    if payment_request_id:
        payment_request = Transaction.objects.get(id=payment_request_id)
        receiver_username = payment_request.receiver.username
        amount = payment_request.amount
        payment_request.delete()

        return render(request, 'financial/payment_confirmation.html', {'receiver_username': receiver_username, 'amount': amount})
    else:
        # Handle case where payment request ID is not found in session
        # Redirect to an appropriate page or display an error message
        return render(request, 'financial/payment_confirmation.html', {'message': 'Payment confirmation not found.'})

    
@login_required
def pay_request(request, request_id):
    try:
        payment_request = PaymentRequest.objects.get(pk=request_id)
        # Placeholder logic to handle payment request
        receiver_username = payment_request.receiver.username  # Update this line
        amount = payment_request.amount
        # Redirect to send payment page with pre-filled information
        return redirect('financial:make_payment_request', receiver_username=receiver_username, amount=amount)
    except PaymentRequest.DoesNotExist:
        messages.error(request, 'Payment request does not exist.')

    return redirect('financial:view_requests')



