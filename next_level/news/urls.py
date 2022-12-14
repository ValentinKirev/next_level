from django.contrib.auth.decorators import login_required
from django.urls import path

from next_level.news.views import NewsAddView, NewsList, NewsDetailsView, NewsEditView, NewsDeleteView

urlpatterns = [
    path('', NewsList.as_view(), name='news list'),
    path('add/', login_required(NewsAddView.as_view()), name='news add'),
    path('details/<slug:slug>/', NewsDetailsView.as_view(), name='news details'),
    path('edit/<slug:slug>/', login_required(NewsEditView.as_view()), name='news edit'),
    path('delete/<slug:slug>/', login_required(NewsDeleteView.as_view()), name='news delete'),
]
