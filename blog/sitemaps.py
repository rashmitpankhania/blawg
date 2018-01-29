from django.contrib.sitemaps import Sitemap
from .models import Post

class Sitemaps(Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return Post.rash.all()

    def lastmod(self, obj):
        return obj.publish