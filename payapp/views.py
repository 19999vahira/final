from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from register.models import Account
from django.contrib.auth import logout
from django.views.decorators.http import require_POST

@login_required
def payapp_home(request):
    try:
        user_account = Account.objects.get(user=request.user)
        account_balance = user_account.balance
        return render(request, 'payapp/home.html', {'account_balance': account_balance})
    except ObjectDoesNotExist:
        return redirect('register:register_choice')



@login_required
def logout_view(request):
    logout(request)
    return redirect('register:register_choice')

