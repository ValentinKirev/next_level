from django.urls import path

from next_level.games.views import GameAddView, GameListView, GameDetailsView, GameEditView, GameDeleteView

urlpatterns = [
    path('', GameListView.as_view(), name='games list'),
    path('add/', GameAddView.as_view(), name='game add'),
    path('details/<str:slug>/', GameDetailsView.as_view(), name='game details'),
    path('edit/<str:slug>/', GameEditView.as_view(), name='game edit'),
    path('delete/<str:slug>/', GameDeleteView.as_view(), name='game delete'),
]
