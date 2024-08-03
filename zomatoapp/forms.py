from django import forms
class inputform(forms.Form):
    user_input=forms.CharField(label='Enter restaurant name:',max_length=100)