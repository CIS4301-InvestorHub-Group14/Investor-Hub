from django.contrib import admin
from .models import Dividends, Institutionalholders, Majorholders, Saveddata, SiteUser, Stock

# Register your models here.
admin.site.register(Stock)
admin.site.register(SiteUser)
admin.site.register(Dividends)
admin.site.register(Institutionalholders)
admin.site.register(Majorholders)
admin.site.register(Saveddata)