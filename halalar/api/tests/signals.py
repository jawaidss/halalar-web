from django.test import TestCase

from . import create_user, create_profile, create_message
from ..signals import send_push_notification

class SendPushNotificationTestCase(TestCase):
    def test_send_push_notification(self):
        sender = create_profile(create_user())
        recipient = create_profile(create_user(1), 1)
        message = create_message(sender, recipient)
        send_push_notification(None, message, True)