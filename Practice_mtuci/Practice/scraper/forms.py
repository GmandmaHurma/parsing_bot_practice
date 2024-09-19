from django import forms

class ScrapeForm(forms.Form):
    query = forms.CharField(label='Наименование', max_length=100, required=True)
    min_salary = forms.IntegerField(label='Мин зарплата', required=False)
