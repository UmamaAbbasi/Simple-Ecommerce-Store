from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from shop.admin import custom_admin_site as admin_site
urlpatterns = [
    path('admin/', admin_site.urls),  # Use custom admin
    path('', include('shop.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

# Media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

