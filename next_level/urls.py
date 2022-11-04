from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('next_level.news.urls')),
    path('games/', include('next_level.games.urls'))
]
