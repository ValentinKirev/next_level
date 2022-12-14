import html

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from next_level.common.forms import SearchForm
from next_level.games.forms import GameCreateForm, GameEditForm, FilterForm
from next_level.games.models import Game
from next_level.utils import UserOwnerMixin


class GameListView(ListView):
    model = Game
    template_name = 'games/games-list-page.html'
    paginate_by = 3
    queryset = model.objects.filter(status='Approved').order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['search_form'] = SearchForm(self.request.GET or None)
        context['filter_form'] = FilterForm(self.request.GET)

        return context

    def get_queryset(self):
        search = self.request.GET.get('title')
        sort_by = self.request.GET.get('sort_by')
        filter_by = self.request.GET.get('filter_by')

        if search:
            self.queryset = self.model.objects.filter(title__icontains=search)

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

        if filter_by:
            self.queryset = self.model.objects.filter(type=filter_by)

        return self.queryset


class GameAddView(PermissionRequiredMixin, CreateView):
    model = Game
    form_class = GameCreateForm
    template_name = 'base/form-page.html'
    success_url = reverse_lazy('games list')
    permission_required = 'games.add_game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['media'] = True
        context['url'] = reverse_lazy('game add')

        return context

    def form_valid(self, form):
        form.instance.author = self.request.user

        if self.request.user.groups.filter(name='Staff').exists() or self.request.user.groups.filter(name='Admin').exists():
            form.instance.status = 'Approved'

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
            if self.request.user.is_authenticated:
                context['user_rating'] = game.rating_set.get(user=self.request.user).rating
        except ObjectDoesNotExist:
            context['user_rating'] = 0
        return context


class GameEditView(PermissionRequiredMixin, UserOwnerMixin, UpdateView):
    model = Game
    form_class = GameEditForm
    template_name = 'base/form-page.html'
    permission_required = 'games.change_game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['media'] = True
        context['url'] = reverse_lazy('game edit', kwargs={
            'slug': self.object.slug
        })
        context['button'] = 'Save Changes'

        return context

    def get_success_url(self):
        return reverse_lazy('game details', kwargs={
            'slug': self.object.slug
        })


class GameDeleteView(PermissionRequiredMixin, UserOwnerMixin, DeleteView):
    model = Game
    success_url = reverse_lazy('games list')
    permission_required = 'games.delete_game'

    def get(self, request, *args, **kwargs):
        game = self.get_object()
        game.rating_set.all().delete()

        categories = game.guidecategory_set.all()

        for category in categories:
            posts = category.guidepost_set.all()

            for post in posts:
                post.guides_like_set.all().delete()

            posts.delete()

        categories.delete()
        game.delete()

        return HttpResponseRedirect(self.success_url)


class GamesWaitingApproveListView(TemplateView):
    model = Game
    template_name = 'games/games-waiting-approve-page.html'

    def get(self, request, *args, **kwargs):
        games_list = self.model.objects.filter(status='Pending').order_by('-id')

        if not request.user.groups.filter(name='Staff').exists() and not request.user.groups.filter(name='Admin').exists():
            return HttpResponseRedirect(reverse_lazy('index'))

        return render(request, self.template_name, context={'games_list': games_list})


class ApproveGameView(PermissionRequiredMixin, UpdateView):
    model = Game
    success_url = reverse_lazy('waiting approve')
    permission_required = 'games.change_game'

    def get(self, request, *args, **kwargs):
        game = self.model.objects.get(slug=self.kwargs['slug'])
        game.status = 'Approved'
        game.save()

        return HttpResponseRedirect(self.success_url)


class RejectGameView(PermissionRequiredMixin, UpdateView):
    model = Game
    success_url = reverse_lazy('waiting approve')
    permission_required = 'games.change_game'

    def get(self, request, *args, **kwargs):
        game = self.model.objects.get(slug=self.kwargs['slug'])
        game.status = 'Rejected'
        game.save()

        return HttpResponseRedirect(self.success_url)
