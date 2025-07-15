from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from . import sitemaps

sitemaps = {
    'static-pages': sitemaps.StaticPagesSitemap,

    'help:list': sitemaps.HelpItemListSitemap,
    'help:detail': sitemaps.HelpItemDetailSitemap,

    'corpus:text-list': sitemaps.CorpusTextListSitemap,
    'corpus:text-detail': sitemaps.CorpusTextDetailSitemap,
}

urlpatterns = i18n_patterns(

    # Custom apps
    path('', include('general.urls')),
    path('account/', include('account.urls')),
    path('corpus/', include('corpus.urls')),
    path('help/', include('help.urls')),

    # CKEditor file uploads
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # Django admin
    path('dashboard/', admin.site.urls),

    # Debug Toolbar
    path('__debug__/', include('debug_toolbar.urls')),

    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # Hide /en/ from all URLs for English pages, so only Persian pages have lang code added to URL
    prefix_default_language=False

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
