# MainApp/forms.py
from django import forms

class DataUploadForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV File')
    timeframe = forms.IntegerField(label='Timeframe (in minutes)')
