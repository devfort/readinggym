from django import forms
import re


class SpeedTestForm(forms.Form):
    seconds = forms.CharField(max_length=10)
    wordcount = forms.IntegerField(widget=forms.HiddenInput(),
                                   min_value=1)

    def clean_seconds(self):
        seconds = self.cleaned_data['seconds']
        match = re.search(r'^(\d+):(\d+(?:\.\d+)?)$', seconds)
        if match:
            minutes, seconds = match.group(1, 2)
            seconds += minutes * 60
        else:
            try:
                seconds = float(seconds)
            except:
                raise forms.ValidationError("Time must be given as seconds")
        if seconds < 0:
            raise forms.ValidationError("A test cannot be completed in negative time")
        if seconds == 0:
            raise forms.ValidationError("A test cannot be completed in no time")

        return seconds
