from django.urls import path

from next_level.games.views import GameAddView

urlpatterns = [
    path('add/', GameAddView.as_view(), name='game add')
]
