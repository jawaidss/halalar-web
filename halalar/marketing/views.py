from django.views.generic.base import TemplateView

class HomeView(TemplateView):
    template_name = 'marketing/home.html'

class AboutView(TemplateView):
    template_name = 'marketing/about.html'

class ContactView(TemplateView):
    template_name = 'marketing/contact.html'

class ThanksView(TemplateView):
    template_name = 'marketing/thanks.html'