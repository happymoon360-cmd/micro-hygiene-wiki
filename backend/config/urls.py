"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.conf.urls.static import serve

from apps.wiki.sitemaps import TipSitemap, CategorySitemap, StaticViewSitemap

SITEMAPS = {
    "tips": TipSitemap,
    "categories": CategorySitemap,
    "static": StaticViewSitemap,
}


def robots_txt(request):
    """
    Serve robots.txt file
    """
    robots_content = """# robots.txt for Micro-Hygiene Wiki
# Allow all web crawlers to access the site

User-agent: *
Allow: /

# Disallow admin area
Disallow: /admin/

# Sitemap location
Sitemap: /sitemap.xml
"""
    return HttpResponse(robots_content, content_type="text/plain")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots.txt", robots_txt),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": SITEMAPS},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
