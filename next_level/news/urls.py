from django.urls import path

from next_level.news.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
