# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# These models are all the table schemas we created in SQLDeveloper


class Stock(models.Model):
    stock_id = models.BigIntegerField(primary_key=True)
    recordtime = models.CharField(max_length=255, blank=True, null=True)
    recordopen = models.FloatField(blank=True, null=True)
    recordclose = models.FloatField(blank=True, null=True)
    recordhigh = models.FloatField(blank=True, null=True)
    recordlow = models.FloatField(blank=True, null=True)
    recordvolume = models.BigIntegerField(blank=True, null=True)
    recorddate = models.DateField()
    timeframe = models.CharField(max_length=3)
    ticker = models.CharField(max_length=4, blank=True, null=True)
    information = models.TextField(blank=True, null=True)
    saveid = models.ForeignKey('Saveddata', models.DO_NOTHING, db_column='saveid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock'


class Dividends(models.Model):
    dividend_id = models.BigIntegerField(primary_key=True)
    recorddate = models.DateField(blank=True, null=True)
    dividend = models.FloatField(blank=True, null=True)
    stock = models.ForeignKey('Stock', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dividends'


class Institutionalholders(models.Model):
    institutional_id = models.BigIntegerField(primary_key=True)
    holder = models.CharField(max_length=255, blank=True, null=True)
    shares = models.BigIntegerField(blank=True, null=True)
    datereported = models.DateField(blank=True, null=True)
    percentout = models.FloatField(blank=True, null=True)
    stock = models.ForeignKey('Stock', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'institutionalholders'


class Majorholders(models.Model):
    major_id = models.BigIntegerField(primary_key=True)
    holder = models.CharField(max_length=255, blank=True, null=True)
    shares = models.BigIntegerField(blank=True, null=True)
    datereported = models.DateField(blank=True, null=True)
    percentout = models.FloatField(blank=True, null=True)
    stock = models.ForeignKey('Stock', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'majorholders'


class Saveddata(models.Model):
    saveid = models.BigIntegerField(primary_key=True)
    diagram = models.BinaryField()
    timeframe = models.CharField(max_length=3)
    metric_type = models.CharField(max_length=255, blank=True, null=True)
    username = models.ForeignKey('SiteUser', models.DO_NOTHING, db_column='username', blank=True, null=True)

    class Meta:
        db_table = 'saveddata'


class SiteUser(models.Model):
    username = models.CharField(primary_key=True, max_length=255)
    password = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'site_user'
