from django import forms
from django.utils.translation import ugettext_lazy as _

from accounts.models import User


class RegistrationForm(forms.ModelForm):

    error_messages = {
            'password_mismatch': _("The two password fields didn't match."),
    }

    password2 = forms.CharField(label=_("Confirm password"),
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "password")
        widgets = {
            "password": forms.PasswordInput
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            mismatch_error = self.error_messages['password_mismatch']
            raise forms.ValidationError(mismatch_error)
        return password2

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
