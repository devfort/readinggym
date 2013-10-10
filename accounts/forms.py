from django import forms

from accounts.models import User


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "password")
        widgets = {
            "password": forms.PasswordInput
        }
