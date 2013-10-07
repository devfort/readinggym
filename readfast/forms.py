from django import forms


class SpeedTestForm(forms.Form):
    seconds = forms.IntegerField()
