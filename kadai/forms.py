from .models import Kadai
from django import forms

class SearchForm(forms.ModelForm):
    class Meta:
        model = Kadai
        fields = ('year','month','words')

    def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'