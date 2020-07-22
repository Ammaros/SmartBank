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

            messages.info(request, "Account Created Sucessfully! Login.")
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
    if request.method == 'POST':

        withdrawAmount = request.POST.get('withdraw')
        depositAmount = request.POST.get('deposit')
        user = User.objects.get(username=request.user.username)
        print(withdrawAmount, depositAmount)


        try:

            if depositAmount == None:

                if user.account.balance >= int(withdrawAmount):

                    user.account.balance = user.account.balance - int(withdrawAmount)
                    user.account.balanceSpent += int(withdrawAmount)
                    user.account.transactions += 1
                    user.account.save()
                    return redirect('dashboard')
                
                else:

                    return redirect('dashboard')
                    messages.error(request, 'Withdraw amount exceeds current balance.')

            elif withdrawAmount == None:

                if int(depositAmount) <= 100000:
                    
                    user.account.balance = user.account.balance + int(depositAmount)
                    user.account.transactions += 1
                    user.account.save()
                    return redirect('dashboard')
                
                else:

                    return redirect('dashboard')
                    messages.error(request, 'Can only deposit a mzximum of Rs. 100,000')
        
        except ValueError:

            return redirect('dashboard')
            messages.error(request, 'Invalid Input! Please try again')

            
    customer = User.objects.all()
    return render(request, 'bankapp/dashboard.html', {'customer': customer})

@login_required(redirect_field_name='login-page')
def transfer(request):
    if request.method == 'POST':

        destUsername = request.POST.get('accountUsername')
        transferAmount = request.POST.get('amount')
        user = User.objects.get(username=request.user.username)
        transferUser = User.objects.get(username=destUsername)

        try:

            if destUsername != '' or transferAmount != None:

                if user.account.balance >= int(transferAmount) and int(transferAmount) <= 100000:

                    user.account.balance = user.account.balance - int(transferAmount)
                    user.account.balanceSpent += int(transferAmount)
                    user.account.transactions += 1
                    transferUser.account.balance = transferUser.account.balance + int(transferAmount)

                    user.account.save()
                    transferUser.account.save()

                    return redirect('transfer')
                    messages.success(request, 'Funds transferred successfully!')
            
                else:

                    return redirect('transfer')
                    messages.error(request, 'Please complete the input fields!')

            else:

                return redirect('transfer')
                messages.error(request, 'Please complete the input fields!')

        except transferUser.DoesNotExist or ValueError:

            return redirect('transfer')
            messages.error(request, 'Invalid input a valid Username or Amount!')

    customer = User.objects.all()
    return render(request, 'bankapp/transfer.html', {'customer': customer})

@login_required(redirect_field_name='login-page')
def transactions(request):
    return render(request, 'bankapp/transactions.html')