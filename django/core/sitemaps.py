from django.contrib.sitemaps import Sitemap
from help import models as help_models
from corpus import models as corpus_models
from django.urls import reverse


class StaticPagesSitemap(Sitemap):
    """
    Sitemap: Static pages that have no data models (e.g. welcome, some about pages, etc.)
    """

    changefreq = "monthly"
    priority = 1.0

    def items(self):
        return [
            'general:welcome',
            'general:about-cite',
            'general:about-credits',
            'general:about-faqs',
            'general:about-glossary',
            'general:about-resources',
            'general:about-technical',
            'general:cookies',
            'general:accessibility',
            'corpus:map-taggedtexts',
            'corpus:map-findspots',
            'corpus:map-placesintexts',
        ]

    def location(self, obj):
        return reverse(obj)


class HelpItemListSitemap(Sitemap):
    """
    Sitemap: HelpItem List
    """

    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['help:list']

    def location(self, obj):
        return reverse(obj)


class HelpItemDetailSitemap(Sitemap):
    """
    Sitemap: HelpItem Detail
    """

    priority = 0.5

    def items(self):
        return help_models.HelpItem.objects.filter(admin_published=True)


class CorpusTextListSitemap(Sitemap):
    """
    Sitemap: Corpus Text List
    """

    changefreq = "daily"
    priority = 1.0

    def items(self):
        return ['corpus:text-list']

    def lastmod(self, obj):
        try:
            return corpus_models.Text.objects.order_by('-meta_created_datetime')[0].meta_created_datetime
        except IndexError:
            return None

    def location(self, obj):
        return reverse(obj)


class CorpusTextDetailSitemap(Sitemap):
    """
    Sitemap: Corpus Text Detail
    """

    priority = 1.0

    def items(self):
        return corpus_models.Text.objects.filter(public_review_approved=True)
