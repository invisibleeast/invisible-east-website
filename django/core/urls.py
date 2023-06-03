from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from . import sitemaps

sitemaps = {
    'static-pages': sitemaps.StaticPagesSitemap,

    # TODO
}

urlpatterns = [
    # Custom apps
    path('', include('general.urls')),
    path('account/', include('account.urls')),
    # path('database/', include('researchdata.urls')),
    # path('help/', include('help.urls')),

    # Django admin
    path('dashboard/', admin.site.urls),

    # Debug Toolbar
    path('__debug__/', include('debug_toolbar.urls')),

    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
