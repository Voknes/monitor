from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages

class Reports(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shpd = models.IntegerField()
    rout = models.IntegerField(null=True, blank=True)
    tv = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('report-add')

class Obhod(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kv = models.IntegerField()
    ne_otkrito = models.IntegerField()
    kv_prezentacii = models.IntegerField()
    kv_zayavki = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('report-add')

class Obzvon(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    zvonki = models.IntegerField()
    nedozvon = models.IntegerField()
    zv_prezentacii = models.IntegerField()
    zv_zayavki = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('report-add')

class Raskleyka(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    doma = models.IntegerField()
    obyavleniya = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('report-add')

class Rating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_shpd = models.IntegerField(default=0)
    faсt_shpd = models.IntegerField(default=0)
    plan_rout = models.IntegerField(default=0)
    faсt_rout = models.IntegerField(default=0)
    plan_pr = models.IntegerField(default=0)
    faсt_pr = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('home')

class CheckIn(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    # img = models.ImageField(upload_to='check/')
    date = models.DateTimeField(default=timezone.now)


class Tarifs(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='tarifs/')
    date = models.DateTimeField(default=timezone.now)