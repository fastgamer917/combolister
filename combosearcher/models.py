from django.db import models
import requests


# Create your models here.

class Combos(models.Model):
    url = models.TextField(verbose_name="Url", blank=True)
    username = models.TextField(verbose_name="Username", blank=True)
    password = models.TextField(verbose_name="Password", blank=True)
    add_date = models.DateTimeField(verbose_name="Added Date", auto_now_add=True, blank=True, null=True)
    source = models.TextField(verbose_name="Data Source", blank=True, null=True)
