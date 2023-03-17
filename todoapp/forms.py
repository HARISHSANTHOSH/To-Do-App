from .models import *
from django import forms
from django .views import generic


class todoform(forms.ModelForm):
    class Meta:
        model=Task
        fields=["title","description","complete"]

