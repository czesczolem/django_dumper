from django.db import models
from django.contrib.auth.models import User


class Dump(models.Model):
    filename = models.CharField(max_length=100, blank=False)
    date = models.DateTimeField()

    def __str__(self):
        return self.filename

    
