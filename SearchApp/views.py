from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm
from .models import SiteUser, Stock


# Create your views here.
# You can find all the html files in the templates file

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard if login is successful
        else:
            # If authentication fails, stay on the login page and show an error message
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html', {'username': username})
    else:
        return render(request, 'login.html')


def register_view(request):
    # if this is a POST request, process form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = SignUpForm(request.POST)
        # check validity
        if form.is_valid():
            # process the data
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )

            site_user = SiteUser.objects.create(
                dob=form.cleaned_data['dob'],
                lastname=form.cleaned_data['lastname'],
                firstname=form.cleaned_data['firstname'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            # redirect to login page in html
            return redirect('login')
    else:
        # The request is GET, so display blank form
        form = SignUpForm()

    return render(request, 'register.html', {"form": form})


# Index will be our welcome page
def index_view(request):
    return render(request, 'index.html')


def home_view(request):
    return render(request, 'dashboard.html')


def settings_view(request):
    return render(request, 'settings.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

def savedcomparisons_view(request):
    return render(request, 'savedcomparisons.html')

def metrics_view(request):
    return render(request, 'metrics.html')

def search_stocks(request):
    if request.method == "POST":
        searchbar = request.POST['searchbar']
        stocks = Stock.objects.filter(ticker__contains=searchbar.upper())

        return render(request, 'search_stocks.html', {'searchbar':searchbar, 'stocks':stocks})
    else:
        return render(request, 'search_stocks.html', {})

def display(request):
    display = Stock.objects.all()
    return render(request, 'display_stocks.html', {'display': display})

def show_stock(request, stock_id):
    stock = Stock.objects.get(pk=stock_id)
    return render(request, 'show_stock.html', {'stock': stock})

# def compare_stocks(request):
#    if request.method == "POST":
#        stock1 = request.POST['stock1']
#        try:
#            stock2 = request.POST['stock2']
#        except:
#            stock2 = None

#    comparison = {stock1, stock2}

#    return render(request, 'compare_stocks.html', {'comparison': comparison})