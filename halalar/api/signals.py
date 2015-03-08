def send_push_notification(sender, instance, created, *args, **kwargs):
    if created:
        instance.send_push_notification()