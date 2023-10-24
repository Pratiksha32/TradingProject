from django import forms

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField(label='CSV File')
    timeframe = forms.IntegerField(label='Timeframe')  # Assuming "timeframe" is an integer



# from django import forms

# class UploadCSVForm(forms.Form):
#     csv_file = forms.FileField()