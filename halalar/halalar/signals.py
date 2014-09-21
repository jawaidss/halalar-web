from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import signals

def create_default_site(app_config, **kwargs):
    if app_config.name == 'django.contrib.sites':
        site_kwargs = {'pk': settings.SITE_ID,
                       'name': settings.SITE_NAME,
                       'domain': settings.SITE_DOMAIN}

        try:
            Site.objects.get(**site_kwargs)
        except Site.DoesNotExist:
            Site.objects.all().delete()
            Site.objects.create(**site_kwargs)

signals.post_migrate.connect(create_default_site)