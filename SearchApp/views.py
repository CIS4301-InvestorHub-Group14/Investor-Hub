from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib import messages
from . import forms, models


#from .forms import SignUpForm
#from .models import SiteUser, Stock


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
        form = forms.SignUpForm(request.POST)
        # check validity
        if form.is_valid():
            # process the data
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )

            site_user = models.SiteUser.objects.create(
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
        form = forms.SignUpForm()

    return render(request, 'register.html', {"form": form})


# Index will be our welcome page
def index_view(request):
    return render(request, 'index.html')


def home_view(request):
    return render(request, 'dashboard.html')


def settings_view(request):
    return render(request, 'settings.html')


def dashboard_view(request):
    if request.method=="POST":
        searchticker=request.POST.get('ticker')
        searchstockid=request.POST.get('stock_id')
        stocksearch=models.Stock.objects.filter(stock_id = searchstockid, ticker=searchticker)
        return render(request,'dashboard.html', {"data": stocksearch})
    else:
        return render(request, 'dashboard.html',{"data": models.Stock.objects.all()})


def savedcomparisons_view(request):
    return render(request, 'savedcomparisons.html')


def metrics_view(request):
    return render(request, 'metrics.html')