from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from myapp.sitemaps import EquipamentoSitemap

sitemaps = {
    'equipamentos': EquipamentoSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('register/', include('accounts.urls')),
    path('', include('myapp.urls')),
    path('frete/', include('frete.urls')),
    path('calendario/', include('calendario.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),  # Adicione isto
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
