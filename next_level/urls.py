from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path, include

from next_level import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('next_level.accounts.urls')),
    path('', include('next_level.news.urls')),
    path('', include('next_level.common.urls')),
    path('games/', include('next_level.games.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
