from django.urls import path

from next_level.games.views import GameAddView, GameListView, GameDetailsView, GameEditView, GameDeleteView, \
    GamesWaitingApproveListView, ApproveGameView, RejectGameView

urlpatterns = [
    path('', GameListView.as_view(), name='games list'),
    path('add/', GameAddView.as_view(), name='game add'),
    path('details/<slug:slug>/', GameDetailsView.as_view(), name='game details'),
    path('edit/<slug:slug>/', GameEditView.as_view(), name='game edit'),
    path('delete/<slug:slug>/', GameDeleteView.as_view(), name='game delete'),
    path('waiting-approve/', GamesWaitingApproveListView.as_view(), name='waiting approve'),
    path('approve/<slug:slug>/', ApproveGameView.as_view(), name='approved'),
    path('reject/<slug:slug>/', RejectGameView.as_view(), name='rejected'),
]
