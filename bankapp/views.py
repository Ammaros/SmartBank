from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from bankapp.forms import SignUpForm, AccountForm
from django.contrib.auth.forms import AuthenticationForm, User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def welcome(request):
    return render(request, 'bankapp/welcome.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        accountForm = AccountForm(request.POST)
        if form.is_valid() and accountForm.is_valid():
            user = form.save()
            account = accountForm.save(commit=False)
            account.user = user
            account.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            return redirect('login-page')
        else:
           messages.error(request, 'Invalid input or missing fields. Please try again!')
           return redirect('signup-page') 
    else:
        form = SignUpForm()
        accountForm = AccountForm()
    return render(request, 'bankapp/signup.html', {'form': form, 'accountForm': accountForm})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request,'Invalid login credentials. Please try agian.')
                return redirect('login-page')
        else:
            messages.error(request,'Invalid login credentials. Please try agian.')
            return redirect('login-page')
    form = AuthenticationForm()
    return render(request, 'bankapp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login-page")

@login_required(redirect_field_name='login-page')
def dashboard(request):
    customer = User.objects.all()
    return render(request, 'bankapp/dashboard.html', {'customer': customer})

@login_required(redirect_field_name='login-page')
def transfer(request):
    return render(request, 'bankapp/transfer.html')

@login_required(redirect_field_name='login-page')
def transactions(request):
    return render(request, 'bankapp/transactions.html')