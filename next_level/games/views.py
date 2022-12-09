from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from next_level.games.forms import GameCreateForm, GameEditForm
from next_level.games.models import Game


class GameListView(ListView):
    model = Game
    template_name = 'games/games-list-page.html'


class GameAddView(CreateView):
    model = Game
    form_class = GameCreateForm
    template_name = 'games/game-add-page.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class GameDetailsView(DetailView):
    model = Game
    template_name = 'games/game-details-page.html'


class GameEditView(UpdateView):
    model = Game
    form_class = GameEditForm
    template_name = 'games/game-edit-page.html'

    def get_success_url(self):
        return reverse_lazy('game details', kwargs={
            'slug': self.object.slug
        })


class GameDeleteView(DeleteView):
    model = Game
    success_url = reverse_lazy('games list')

    def get(self, request, *args, **kwargs):
        self.get_object().delete()

        return HttpResponseRedirect(self.success_url)
