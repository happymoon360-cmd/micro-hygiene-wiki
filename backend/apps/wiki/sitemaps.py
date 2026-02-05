"""
Sitemap generator for wiki application
Generates clean, SEO-friendly URLs with lowercase, hyphen-separated slugs
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Tip, Category


class TipSitemap(Sitemap):
    """
    Sitemap for Tip pages with clean, SEO-friendly URLs
    Format: /tips/:id-:slug (e.g., /tips/123-how-to-clean-kitchen)
    """

    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Tip.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        """
        Generate clean URL format: /tips/:id-:slug
        Example: /tips/123-how-to-clean-kitchen
        """
        slug = self._create_slug(obj.title)
        return f"/tips/{obj.id}-{slug}"

    def _create_slug(self, text):
        """
        Convert title to lowercase, hyphen-separated slug
        Example: "How to Clean Kitchen" -> "how-to-clean-kitchen"
        """
        import re

        slug = text.lower()
        slug = re.sub(r"[^\w\s-]", "", slug)
        slug = re.sub(r"[\s_]+", "-", slug)
        slug = re.sub(r"-+", "-", slug)
        slug = slug.strip("-")
        return slug


class CategorySitemap(Sitemap):
    """
    Sitemap for Category pages with clean URLs
    Format: /categories/:slug (e.g., /categories/kitchen)
    """

    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return None

    def location(self, obj):
        """
        Generate clean URL format: /categories/:slug
        Example: /categories/kitchen
        """
        return f"/categories/{obj.slug}"


class StaticViewSitemap(Sitemap):
    """
    Sitemap for static pages like home, about, etc.
    """

    priority = 0.5
    changefreq = "daily"

    def items(self):
        return ["home", "about", "categories"]

    def location(self, item):
        if item == "home":
            return "/"
        return f"/{item}/"
