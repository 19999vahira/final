from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Account


def register_choice(request):
    return render(request, 'register/register_choice.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            currency = request.POST.get('currency')  # Get selected currency from form
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                Account.objects.create(user=user, currency=currency)
                return redirect('payapp:payapp_home')  # Redirect to presentation layer upon successful sign-up
    else:
        form = UserCreationForm()
    return render(request, 'register/signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('payapp:payapp_home')  # Redirect to presentation layer upon successful sign-in
        else:
            messages.error(request, 'Invalid username or password. Please try again or sign up.')
    else:
        # If user is already authenticated, redirect to payapp_home
        if request.user.is_authenticated:
            return redirect('payapp:payapp_home')
    return render(request, 'register/signin.html')

