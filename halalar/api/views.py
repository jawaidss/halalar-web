from braces.views import CsrfExemptMixin, JSONResponseMixin
from push_notifications.models import APNSDevice, GCMDevice

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator

from .forms import UserForm, ProfileForm, AuthenticationForm, MessageForm, APNSDeviceForm, GCMDeviceForm
from .models import Profile, Message

class API(CsrfExemptMixin, JSONResponseMixin, View):
    def render_json_response(self, *args, **kwargs):
        response = super(API, self).render_json_response(*args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        return response

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
                return self.error('This profile is inactive.')
            else:
                return self.success({'token': profile.token})
        else:
            return self.error(form.error_message())

class SignUpAPI(API):
    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            profile.send_delayed_welcome_email()
            profile.send_signup_notification_email()
            profile.subscribe_to_mailchimp_list()

            return self.success({'token': profile.token})
        else:
            error_messages = [user_form.error_message(), profile_form.error_message()]
            error_message = '\n'.join(error_messages).strip()

            return self.error(error_message)

class AuthenticatedAPI(API):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user__is_active=True, token=getattr(request, request.method, {}).get('token'))

        return super(AuthenticatedAPI, self).dispatch(request, profile, *args, **kwargs)

class GetProfileAPI(AuthenticatedAPI):
    random = False

    def get(self, request, profile, *args, **kwargs):
        if self.random:
            profiles = Profile.objects.filter(user__is_active=True).exclude(gender=profile.gender)

            if profiles.exists():
                username = self.kwargs.get('username')

                if username is None:
                    profile = profiles.order_by('?')[0]
                else:
                    profile = get_object_or_404(profiles, user__username=username)
            else:
                return self.error('No profiles yet')

        return self.success({'profile': profile.serialize(not self.random)})

class EditProfileAPI(AuthenticatedAPI):
    def post(self, request, profile, *args, **kwargs):
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            profile = form.save()

            return self.success({})
        else:
            return self.error(form.error_message())

class GetConversationsAPI(AuthenticatedAPI):
    def get(self, request, profile, *args, **kwargs):
        sent = set(profile.sent.filter(recipient__user__is_active=True).values_list('recipient__user__username', flat=True))
        received = set(profile.received.filter(sender__user__is_active=True).values_list('sender__user__username', flat=True))
        pks = []

        for username in sent | received:
            q = Q(recipient__user__username=username, sender=profile) |\
                Q(sender__user__username=username, recipient=profile)
            pk = Message.objects.filter(q).latest().pk
            pks.append(pk)

        messages = Message.objects.filter(pk__in=pks).reverse()
        messages = [message.serialize() for message in messages]

        return self.success({'messages': messages})

class GetConversationAPI(AuthenticatedAPI):
    def get(self, request, profile, *args, **kwargs):
        username = self.kwargs['username']
        q = Q(recipient__user__is_active=True, recipient__user__username=username, sender=profile) |\
            Q(sender__user__is_active=True, sender__user__username=username, recipient=profile)
        messages = Message.objects.filter(q)
        messages = [message.serialize() for message in messages]

        return self.success({'messages': messages})

class SendMessageAPI(AuthenticatedAPI):
    def post(self, request, profile, *args, **kwargs):
        profiles = Profile.objects.filter(user__is_active=True).exclude(gender=profile.gender)
        username = self.kwargs['username']
        recipient = get_object_or_404(profiles, user__username=username)
        form = MessageForm(data=request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = profile
            message.recipient = recipient
            message.save()

            return self.success({'message': message.serialize()})
        else:
            return self.error(form.error_message())

class RegisterPushNotificationsAPI(AuthenticatedAPI):
    def post(self, request, profile, *args, **kwargs):
        platform = self.kwargs['platform']
        Device = {'iOS': APNSDevice, 'Android': GCMDevice}[platform]
        DeviceForm = {'iOS': APNSDeviceForm, 'Android': GCMDeviceForm}[platform]
        registration_id = request.POST.get('registration_id')

        try:
            device = Device.objects.get(registration_id=registration_id)
        except Device.DoesNotExist:
            device = None

        form = DeviceForm(request.POST, instance=device)

        if form.is_valid():
            device = form.save()
            device.user = profile.user
            device.save()

            return self.success({})
        else:
            return self.error(form.error_message())