from django.conf import settings
from django.contrib.sites.models import Site
from django.db import migrations

def create_default_site(*args, **kwargs):
    Site.objects.all().delete()
    Site.objects.create(pk=settings.SITE_ID,
                        name=settings.SITE_NAME,
                        domain=settings.SITE_DOMAIN)

class Migration(migrations.Migration):
    dependencies = [
        ('api', '0001_initial'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_site),
    ]