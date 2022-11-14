from django.urls import path

from next_level.news.views import IndexView, OtherView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('other/', OtherView.as_view(), name='other')
]
