from django.views.generic import CreateView

from next_level.games.forms import GameCreateForm
from next_level.games.models import Game


class GameAddView(CreateView):
    model = Game
    form_class = GameCreateForm
