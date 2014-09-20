from braces.views import CsrfExemptMixin, JSONResponseMixin

from django.views.generic import View

from .forms import UserForm, ProfileForm, AuthenticationForm
from .models import Profile

class API(CsrfExemptMixin, JSONResponseMixin, View):
    def success(data):
        return self.render_json_response({'status': 'success', 'data': data})

    def error(message):
        return self.render_json_response({'status': 'error', 'message': message})

class LogInAPI(API):
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            try:
                profile = form.get_user().profile
            except Profile.DoesNotExist:
                return self.error('') # TODO
            else:
                return self.success({'token': profile.token})
        else:
            return self.error(form.error_message())

class SignUpAPI(API):
    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            # TODO
            # 1) Send emails to admins.
            # 2) Send delayed email to user.
            # 3) Add user to MailChimp list.

            return self.success({'token': profile.token})
        else:
            error_messages = [user_form.error_message(), profile_form.error_message()]
            error_message = '\n'.join(error_messages).strip()

            return self.error(error_message)