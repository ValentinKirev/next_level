from django.urls import path, include

from next_level.news.views import IndexView, NewsAddView, NewsList, NewsDetailsView, NewsEditView, NewsDeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('news/', include([
        path('', NewsList.as_view(), name='news list'),
        path('add/', NewsAddView.as_view(), name='news add'),
        path('details/<str:slug>/', NewsDetailsView.as_view(), name='news details'),
        path('edit/<str:slug>/', NewsEditView.as_view(), name='news edit'),
        path('delete/<str:slug>/', NewsDeleteView.as_view(), name='news delete'),
    ]))
]
