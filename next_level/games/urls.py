from django.contrib.auth.decorators import login_required
from django.urls import path

from next_level.games.views import GameAddView, GameListView, GameDetailsView, GameEditView, GameDeleteView, \
    GamesWaitingApproveListView, ApproveGameView, RejectGameView

urlpatterns = [
    path('', GameListView.as_view(), name='games list'),
    path('add/', login_required(GameAddView.as_view()), name='game add'),
    path('details/<slug:slug>/', GameDetailsView.as_view(), name='game details'),
    path('edit/<slug:slug>/', login_required(GameEditView.as_view()), name='game edit'),
    path('delete/<slug:slug>/', login_required(GameDeleteView.as_view()), name='game delete'),
    path('waiting-approve/', login_required(GamesWaitingApproveListView.as_view()), name='waiting approve'),
    path('approve/<slug:slug>/', login_required(ApproveGameView.as_view()), name='approved'),
    path('reject/<slug:slug>/', login_required(RejectGameView.as_view()), name='rejected'),
]
