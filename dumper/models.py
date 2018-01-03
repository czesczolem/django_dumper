from django.db import models

class Dump(models.model):
    filename = models.CharField(max_length=100, blank=False)
    date = models.DateTimeField()

    def __str__(self):
        return self.filename
