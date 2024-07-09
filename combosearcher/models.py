from django.db import models


# Create your models here.

class Combos(models.Model):
    combo = models.TextField(verbose_name="Full combo url:u:p", blank=True)
    add_date = models.DateTimeField(verbose_name="Added Date", auto_now_add=True, blank=True, null=True)
    source = models.TextField(verbose_name="Data Source", blank=True, null=True)
