from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^log-in/$', views.LogInAPI.as_view(), name='api-log_in'),
    url(r'^sign-up/$', views.SignUpAPI.as_view(), name='api-sign_up'),
    url(r'^get-profile/$', views.GetProfileAPI.as_view(), name='api-get_profile'),
    url(r'^get-profile/random/$', views.GetProfileAPI.as_view(random=True), name='api-get_random_profile'),
    url(r'^get-profile/random/(?P<username>\w+)/$', views.GetProfileAPI.as_view(random=True), name='api-get_specific_profile'),
    url(r'^edit-profile/$', views.EditProfileAPI.as_view(), name='api-edit_profile'),
    url(r'^get-conversations/$', views.GetConversationsAPI.as_view(), name='api-get_conversations'),
    url(r'^get-conversation/(?P<username>\w+)/$', views.GetConversationAPI.as_view(), name='api-get_conversation'),
    url(r'^send-message/(?P<username>\w+)/$', views.SendMessageAPI.as_view(), name='api-send_message'),
    url(r'^register-push-notifications/(?P<platform>(iOS|Android))/$', views.RegisterPushNotificationsAPI.as_view(), name='api-register_push_notifications'),
]