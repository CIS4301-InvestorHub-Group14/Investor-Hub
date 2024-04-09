from django.shortcuts import render

# Create your views here.
# You can find all the html files in the templates file
def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

# Index will be our welcome page
def index_view(request):
    return render(request, 'index.html')

def home_view(request):
    return render(request, 'dashboard.html')

def settings_view(request):
    return render(request, 'settings.html')