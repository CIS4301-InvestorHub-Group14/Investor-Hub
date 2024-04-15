"""
URL configuration for InvestorHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from SearchApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.index_view, name='index'),
    path('settings/', views.settings_view, name='settings'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('savedcomparisons/', views.savedcomparisons_view, name='savedcomparisons'),
    path('metrics/', views.metrics_view, name='metrics'),
    path('company/<company>/', views.company_view, name='company'),
    path('company/<company>/<datametric>', views.datametric_view, name='datametric'),

]
