import html

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from next_level.common.forms import SearchForm
from next_level.games.forms import GameCreateForm, GameEditForm, FilterForm
from next_level.games.models import Game


class GameListView(ListView):
    model = Game
    template_name = 'games/games-list-page.html'
    paginate_by = 3
    queryset = Game.objects.all().order_by('-id')
    form_class = SearchForm
    params = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = self.form_class()
        context['filter_form'] = FilterForm()
        context['params'] = self.params

        return context

    def get_queryset(self):
        search = self.request.GET.get('title')
        sort_by = self.request.GET.get('sort_by')
        filter_by = self.request.GET.get('filter_by')

        if search:
            self.queryset = self.model.objects.filter(title__icontains=search)
            self.params += f'&title={search}'

        if sort_by:
            if sort_by == 'Max Level ' + html.unescape('&#8593;'):
                self.queryset = self.model.objects.order_by('max_level')
            elif sort_by == 'Max Level ' + html.unescape('&#8595;'):
                self.queryset = self.model.objects.order_by('-max_level')
            elif sort_by == 'Rating ' + html.unescape('&#8593;'):
                self.queryset = self.model.objects.order_by('average_rating')
            elif sort_by == 'Rating ' + html.unescape('&#8595;'):
                self.queryset = self.model.objects.order_by('-average_rating')
            elif sort_by == 'Release Date ' + html.unescape('&#8593;'):
                self.queryset = self.model.objects.order_by('release_date')
            elif sort_by == 'Release Date ' + html.unescape('&#8595;'):
                self.queryset = self.model.objects.order_by('-release_date')

            self.params += f'&sort_by={sort_by}'

        if filter_by:
            self.queryset = self.model.objects.filter(type=filter_by)
            self.params += f'&filter_by={filter_by}'

        return self.queryset


class GameAddView(CreateView):
    model = Game
    form_class = GameCreateForm
    template_name = 'games/game-add-page.html'
    success_url = reverse_lazy('games list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class GameDetailsView(DetailView):
    model = Game
    template_name = 'games/game-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        game = self.get_object()
        ratings = game.rating_set.all()
        rates_count = game.rating_set.count()

        total_rating = 0

        for rating in ratings:
            total_rating += rating.rating

        context['rates_count'] = rates_count

        try:
            context['user_rating'] = game.rating_set.get(user=self.request.user).rating
        except ObjectDoesNotExist:
            context['user_rating'] = 0
        return context


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
        game = self.get_object()
        game.rating_set.all().delete()
        game.delete()

        return HttpResponseRedirect(self.success_url)
