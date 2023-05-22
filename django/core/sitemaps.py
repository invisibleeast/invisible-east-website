from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticPagesSitemap(Sitemap):
    """
    Sitemap: Static pages that have no data models (e.g. welcome, some about pages, etc.)
    """

    changefreq = "monthly"
    priority = 1.0

    def items(self):
        return ['general:welcome',
                'general:about',
                'general:cookies',
                'general:accessibility']

    def location(self, obj):
        return reverse(obj)
