from .models import Kadai
from django import forms
import datetime

class SearchForm(forms.ModelForm):
    year = forms.ChoiceField(label='年',choices=[(year, year) for year in range(2018, datetime.datetime.now().year + 1)])
    month = forms.ChoiceField(label='月',choices=[(month, month) for month in range(1, 13)])

    class Meta:
        model = Kadai
        fields = ['year', 'month', 'words']