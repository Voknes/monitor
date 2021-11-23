from django.db import models
from django.conf import settings
from django.utils import timezone
from django.shortcuts import reverse

class Address(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=40)
    date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('home')
