from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

class SimpleSitemap(Sitemap):
    def items(self):
        return (
            'marketing-home',
            'marketing-about',
            'marketing-contact',
            'marketing-thanks',
            'legal-privacy_policy',
            'legal-terms_of_service',
            'admin:index',
        )

    def location(self, name):
        return reverse(name)

sitemaps = {
    'simple_sitemap': SimpleSitemap,
}