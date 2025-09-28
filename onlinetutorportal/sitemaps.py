from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    def items(self):
        return ['home', 'contact']  # remove 'about' if not created

    def location(self, item):
        return reverse(item)
