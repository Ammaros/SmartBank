import datetime
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

            user = User.objects.get(username=request.user.username)
            user.account.history = user.account.history.remove('')
            user.account.save()

            messages.info(request, "Account Created Sucessfully! Login.")
            return redirect('login-page')
        else:
           messages.warning(request, 'Invalid input or missing fields. Please try again!')
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
                messages.warning(request,'Invalid login credentials. Please try agian.')
                return redirect('login-page')
        else:
            messages.warning(request,'Invalid login credentials. Please try agian.')
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

        try:

            if depositAmount == None:

                if user.account.balance >= int(withdrawAmount):

                    date = datetime.date.today()

                    user.account.balance = user.account.balance - int(withdrawAmount)
                    user.account.balanceSpent += int(withdrawAmount)
                    user.account.transactions += 1
                    user.account.history.append(f'{date}: Withdrew Rs. {withdrawAmount}')
                    user.account.save()
                    return redirect('dashboard')
                
                else:
                    
                    messages.warning(request, 'Withdraw amount exceeds current balance.')
                    return redirect('dashboard')

            elif withdrawAmount == None:

                if int(depositAmount) <= 100000:

                    date = datetime.date.today()
                    
                    user.account.balance = user.account.balance + int(depositAmount)
                    user.account.transactions += 1
                    user.account.history.append(f'{date}: Deposited Rs. {depositAmount}')
                    user.account.save()
                    return redirect('dashboard')
                
                else:

                    messages.warning(request, 'Can only deposit a maximum of Rs. 100,000')
                    return redirect('dashboard')
        
        except ValueError:

            messages.warning(request, 'Input Valid Amount')
            return redirect('dashboard')

            
    customer = User.objects.all()
    return render(request, 'bankapp/dashboard.html', {'customer': customer})

@login_required(redirect_field_name='login-page')
def transfer(request):
    if request.method == 'POST':

        destUsername = request.POST.get('accountUsername')
        transferAmount = request.POST.get('amount')

        try:

            user = User.objects.get(username=request.user.username)
            transferUser = User.objects.get(username=destUsername)

        except User.DoesNotExist:

            messages.warning(request, 'User does not exist!')
            return redirect('transfer')

        try:

                if user.account.balance >= int(transferAmount) and int(transferAmount) <= 100000:

                    date = datetime.date.today()

                    user.account.balance = user.account.balance - int(transferAmount)
                    user.account.balanceSpent += int(transferAmount)
                    user.account.transactions += 1
                    user.account.history.append(f'{date}: Transferred Rs. {transferAmount} to {transferUser}')
                
                    transferUser.account.balance = transferUser.account.balance + int(transferAmount)
                    transferUser.account.transactions += 1
                    transferUser.account.history.append(f'{date}: Recieved Rs. {transferAmount} from {user}')

                    user.account.save()
                    transferUser.account.save()

                    messages.success(request, 'Funds transferred successfully!')
                    return redirect('transfer')
            
                else:

                    messages.warning(request, 'Amount out of bounds!')
                    return redirect('transfer')

        except ValueError:

            messages.warning(request, 'Input Valid Amount!')
            return redirect('transfer')

    customer = User.objects.all()
    return render(request, 'bankapp/transfer.html', {'customer': customer})

@login_required(redirect_field_name='login-page')
def transactions(request):
    user = User.objects.get(username=request.user.username)

    if len(user.account.history) > 10:
        sliceValue = len(user.account.history) - 10
        user.account.history = user.account.history[sliceValue:]
        user.account.save()

    customer = User.objects.all()
    return render(request, 'bankapp/transactions.html', {'customer': customer})