from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm
from .models import SiteUser, Stock
from django.db import connection
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
from matplotlib.backends.backend_agg import FigureCanvasAgg
from datetime import date
import matplotlib

matplotlib.use('agg')
from django.http import HttpResponse


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

            SiteUser.objects.create(
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
    context = {'errorMessage': ''}
    if request.method == "POST":
        company = request.POST['company']
        companyMatch = Stock.objects.filter(ticker=company)[0]

        if companyMatch:
            return redirect('company', company=company)
        else:
            context = {'errorMessage': 'Invalid Company Name'}
            pass

    return render(request, 'dashboard.html', context)


def savedcomparisons_view(request):
    return render(request, 'savedcomparisons.html')


def metrics_view(request):
    return render(request, 'metrics.html')


def company_view(request, company):
    if request.method == "POST":
        datametric = request.POST.get('data-metrics')
        d1 = request.POST.get('d1')
        m1 = request.POST.get('m1')
        y1 = request.POST.get('y1')
        d2 = request.POST.get('d2')
        m2 = request.POST.get('m2')
        y2 = request.POST.get('y2')

        if len(d1) == 1:
            d1 = d1.zfill(2)
        if len(m1) == 1:
            m1 = m1.zfill(2)
        if len(d2) == 1:
            d2 = d2.zfill(2)
        if len(m2) == 1:
            m2 = m2.zfill(2)

        t1 = y1 + '-' + m1 + '-' + d1
        t2 = y2 + '-' + m2 + '-' + d2

        #just testing
        getRSI(company, t1, t2)

        if datametric:
            return redirect('datametric', company=company, datametric=datametric)
        else:
            # context = {'errorMessage': 'Invalid Company Name'}
            pass

    return render(request, 'company.html', {'companyName': company})


def getMMA(ticker, t1, t2):
    with connection.cursor() as cursor:
        query = '''
                SELECT newdate, ROUND(AVG(RECORDCLOSE),2) FROM
                (SELECT STOCK_ID,RECORDCLOSE,RECORDDATE, ltrim(TO_CHAR(RECORDDATE,'mm-yyyy'),'0') AS newdate FROM STOCK
                WHERE TICKER = %s AND
                RECORDDATE BETWEEN TO_DATE(%s,'YYYY-MM-DD') AND TO_DATE(%s,'YYYY-MM-DD'))
                GROUP BY newdate
        '''

        cursor.execute(query, (ticker, t1, t2))
        rows = cursor.fetchall()


def getMACD(ticker, t1, t2):
    with connection.cursor() as cursor:
        query = '''
                    SELECT RECORDDATE,gnum, 
                    CASE WHEN ema = 0 THEN (RECORDCLOSE * (2/27) + LAG(ema,1,0) OVER (ORDER BY gnum)*(1-2/27))
                    ELSE ema
                    END AS ema2
                    FROM(
                    SELECT RECORDDATE, RECORDCLOSE,gnum,
                    CASE WHEN gnum = 1 THEN 
                    (
                    SELECT AVG(RECORDCLOSE) FROM(
                    SELECT RECORDDATE, RECORDCLOSE,FLOOR((ROW_NUMBER() OVER (ORDER BY RECORDDATE)-1) / 26) + 1 AS gnum
                    FROM STOCK WHERE TICKER = %s AND
                    RECORDDATE BETWEEN TO_DATE(%s,'YYYY-MM-DD') AND TO_DATE(%s,'YYYY-MM-DD'))
                    GROUP BY GNUM
                    FETCH FIRST 1 ROWS ONLY)
                    ELSE 0
                    END AS ema
                    FROM(
                    SELECT RECORDDATE, RECORDCLOSE,FLOOR((ROW_NUMBER() OVER (ORDER BY RECORDDATE)-1) / 26) + 1 AS gnum,
                    ROW_NUMBER() OVER (ORDER BY (RECORDDATE)) AS rnum
                    FROM STOCK WHERE TICKER = %s AND
                    RECORDDATE BETWEEN TO_DATE(%s,'YYYY-MM-DD') AND TO_DATE(%s,'YYYY-MM-DD')))
                    WHERE gnum != 1
        '''

        cursor.execute(query, (ticker, t1, t2, ticker, t1, t2))
        row = cursor.fetchall()


def getVolatility(ticker, t1, t2):
    with connection.cursor() as cursor:
        query = '''
                    SELECT NEWDATE, ROUND((s / c),2)
                    FROM(
                    SELECT NEWDATE,COUNT(*) as c ,SUM(rdiff) as s
                    FROM(
                    SELECT NEWDATE, POWER((RECORDCLOSE - avgclose),2) as rdiff FROM
                    (
                    SELECT NEWDATE,RECORDCLOSE, AVG(RECORDCLOSE) OVER (PARTITION BY newdate) avgclose 
                    FROM
                    (
                    SELECT STOCK_ID,RECORDCLOSE,RECORDDATE, ltrim(TO_CHAR(RECORDDATE,'mm-yyyy'),'0') AS newdate FROM STOCK 
                    WHERE TICKER = %s AND
                    RECORDDATE BETWEEN TO_DATE(%s,'YYYY-MM-DD') AND TO_DATE(%s,'YYYY-MM-DD')
                    )
                    )
                    )
                    GROUP BY NEWDATE
                    )
            '''

        cursor.execute(query, (ticker, t1, t2))
        cursor.execute(query, (ticker, t1, t2))
        row = cursor.fetchall()


def getRSI(ticker, t1, t2):
    with connection.cursor() as cursor:
        query = '''
                    SELECT newdate, 
                    CASE WHEN ad = 0 THEN ((100 - (100 / (1+au))))
                        ELSE (100 - (100 / (1+(au / ad))))
                    END AS rsi
                    FROM(
                    SELECT newdate, AVG(U) as au, AVG(D) as ad
                    FROM(
                    SElECT RECORDDATE,newdate, 
                    CASE WHEN RECORDCLOSE > price_prev THEN (RECORDCLOSE - price_prev)
                        ELSE 0
                    END AS U,
                    CASE WHEN RECORDCLOSE < price_prev THEN ABS(RECORDCLOSE - price_prev)
                        ELSE 0
                    END AS D
                    FROM
                    (SELECT STOCK_ID,RECORDCLOSE,RECORDDATE, ltrim(TO_CHAR(RECORDDATE,'mm-yyyy'),'0') AS newdate, LAG(RECORDCLOSE, 1, RECORDCLOSE) OVER (ORDER BY RECORDDATE) AS price_prev
                    FROM STOCK 
                    WHERE TICKER = %s AND
                    RECORDDATE BETWEEN TO_DATE(%s,'YYYY-MM-DD') AND TO_DATE(%s,'YYYY-MM-DD')))
                    GROUP BY newdate)
            '''

        cursor.execute(query, (ticker, t1, t2))
        rows = cursor.fetchall()
        nrows = []
        for r in rows:
            mth = (int)(rows[0][0].split('-')[0])
            yr = (int)(rows[0][0].split('-')[1])
            day = 1
            new_date = date(yr, mth, day)


def datametric_view(request, company, datametric):

    return render(request, "datametric.html")
