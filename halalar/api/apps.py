from django.apps import AppConfig
from django.db.models.signals import post_save

from .signals import send_push_notification

class APIConfig(AppConfig):
    name = 'api'
    verbose_name = 'API'

    def ready(self):
        Message = self.get_model('Message')
        post_save.connect(send_push_notification, sender=Message)