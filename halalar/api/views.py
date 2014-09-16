from braces.views import CsrfExemptMixin, JSONResponseMixin

from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import View

from .forms import UserForm, ProfileForm

class API(CsrfExemptMixin, JSONResponseMixin, View):
    pass

class LogInAPI(API):
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            token = form.get_user().profile.token # TODO: Profile.DoesNotExist

            return self.render_json_response({'token': token})
        else:
            return self.render_json_response(form.errors)

class SignUpAPI(API):
    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return self.render_json_response({'token': profile.token})
        else:
            errors = {}
            errors.update(user_form.errors)
            errors.update(profile_form.errors)

            return self.render_json_response(errors)