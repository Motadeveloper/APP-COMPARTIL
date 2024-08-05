from django.contrib.sitemaps import Sitemap
from .models import Equipamento

class EquipamentoSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Equipamento.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
