from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class SaveAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    saved_date = models.DateTimeField(auto_now_add=True)
    saved_data = models.JSONField(null=True, blank=True)
    saved_query = models.CharField(max_length=200, null=True, blank=True)
    summary = models.TextField( null=False, blank=False)
