from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from .models import SiteUser


# Create your views here.
# You can find all the html files in the templates file


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # redirect to user's home page
        else:
            # Invalid login
            pass

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