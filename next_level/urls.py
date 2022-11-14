from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('next_level.accounts.urls')),
    path('', include('next_level.news.urls'))
]
