from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse

from accounts.models import User
from accounts.forms import RegistrationForm


class RegisterView(CreateView):

    form_class = RegistrationForm
    template_name = "registration/register.html"
    model = User

    def get_success_url(self):
        # Using the method rather than the class member here, because we import
        # this from speedreader/urls.py, at which point there are no URLs
        return reverse("dashboard")

