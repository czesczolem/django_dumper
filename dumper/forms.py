from django.forms import ModelForm
from . models import Dump
import datetime

class DumpForm(ModelForm):
    class Meta:
        model = Dump
        fields = ['filename']
        date = datetime.datetime.now()



