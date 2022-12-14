from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path, include

from next_level import settings
from next_level.custom_handlers import page_not_found, permission_denied, bad_request, internal_server_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('next_level.common.urls')),
    path('news/', include('next_level.news.urls')),
    path('accounts/', include('next_level.accounts.urls')),
    path('games/', include('next_level.games.urls')),
    path('guides/', include('next_level.guides.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler403 = permission_denied
handler404 = page_not_found
handler400 = bad_request
handler500 = internal_server_error
