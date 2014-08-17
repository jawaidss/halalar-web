from datetime import date

from django.contrib.sites.models import Site

def site(request):
    return {'site': Site.objects.get_current()}

def today(request):
    return {'today': date.today()}