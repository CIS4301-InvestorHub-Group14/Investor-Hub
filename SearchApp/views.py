from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import SignUpForm

# Create your views here.
# You can find all the html files in the templates file
def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    # if this is a POST request, process form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = SignUpForm(request.POST)
        # check validity
        if form.is_valid():
            # process the data

            # redirect to login page
            return HttpResponseRedirect("login/")

    return render(request, 'register.html', {"form": form})

# Index will be our welcome page
def index_view(request):
    return render(request, 'index.html')

def home_view(request):
    return render(request, 'dashboard.html')

def settings_view(request):
    return render(request, 'settings.html')