from braces.views import CsrfExemptMixin, JSONResponseMixin

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator

from .forms import UserForm, ProfileForm, AuthenticationForm
from .models import Profile

class API(CsrfExemptMixin, JSONResponseMixin, View):
    def success(self, data):
        return self.render_json_response({'status': 'success', 'data': data})

    def error(self, message):
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

class AuthenticatedAPI(API):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, token=getattr(request, request.method, {}).get('token'))

        return super(AuthenticatedAPI, self).dispatch(request, profile, *args, **kwargs)

class GetProfileAPI(AuthenticatedAPI):
    random = False

    def get(self, request, profile, *args, **kwargs):
        if self.random:
            profiles = Profile.objects.exclude(gender=profile.gender) # TODO

            if profiles.exists():
                username = self.kwargs.get('username')

                if username is None:
                    profile = profiles.order_by('?')[0]
                else:
                    profile = get_object_or_404(profiles, user__username=username)
            else:
                return self.error('') # TODO

        return self.success({'profile': profile.serialize(not self.random)})

class EditProfileAPI(AuthenticatedAPI):
    def post(self, request, profile, *args, **kwargs):
        form = ProfileForm(request.POST, instance=profile)
        del form.fields['gender'] # TODO

        if form.is_valid():
            profile = form.save()

            return self.success({'profile': profile.serialize()})
        else:
            return self.error(form.error_message())