# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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
    date_reported = models.DateField(blank=True, null=True)
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


class SiteUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class SiteUser(models.Model):
    username = models.CharField(primary_key=True, max_length=255)
    password = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)

    objects = SiteUserManager()

    USERNAME_FIELDS = 'username'
    REQUIRED_FIELDS = ['email']
    class Meta:
        db_table = 'site_user'

    def __str__(self):
        return self.username
