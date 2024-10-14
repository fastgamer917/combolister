from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Combos(models.Model):
    combo = models.TextField(verbose_name="Full combo url:u:p", blank=True)
    add_date = models.DateTimeField(verbose_name="Added Date", auto_now_add=True, blank=True, null=True)
    source = models.TextField(verbose_name="Data Source", blank=True, null=True)

class SearchProgress(models.Model):
    submitted_user = models.ForeignKey(User, verbose_name="User who submitted the request", on_delete=models.CASCADE)
    search_term = models.TextField(verbose_name="Search term", blank=True)
    submitted_time = models.DateTimeField(verbose_name="Search Submitted Time", auto_now_add=True, blank=True, null=True)
    search_status = models.TextField(verbose_name="Search Status", blank=True)
    search_completed_time = models.DateTimeField(verbose_name="Search Completed Time", auto_now_add=True, blank=True, null=True)
    run_time = models.FloatField(verbose_name="Search Run Time", blank=True, null=True)
    total_found = models.IntegerField(verbose_name="Total Found Results", blank=True, null=True)

    def __str__(self):
        return f"{self.submitted_user} - {self.search_term}"

class SearchResult(models.Model):
    search_id = models.ForeignKey(SearchProgress, verbose_name="Search ID from progress", on_delete=models.CASCADE)
    found_string = models.TextField(verbose_name="Found Combo", blank=True)
    found_in_file = models.TextField(verbose_name="Found in File", blank=True)

    def __str__(self):
        return f"{self.found_string} - {self.found_in_file}"

class LogsFolderPath(models.Model):
    folder_path = models.TextField(verbose_name="Folder Path", blank=True)
    is_active = models.BooleanField(verbose_name="Is Active", default=True)

    def __str__(self):
        return f"{self.folder_path} - {self.is_active}"
