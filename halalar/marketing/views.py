from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy

from .forms import ContactForm

class HomeView(TemplateView):
    template_name = 'marketing/home.html'

class AboutView(TemplateView):
    template_name = 'marketing/about.html'

class ContactView(FormView):
    template_name = 'marketing/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('marketing-thanks')

    def form_valid(self, form):
        form.send_mail(self.request.META['REMOTE_ADDR'])
        return super(ContactView, self).form_valid(form)

class ThanksView(TemplateView):
    template_name = 'marketing/thanks.html'