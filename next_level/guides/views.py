from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, TemplateView

from next_level.common.forms import SearchForm
from next_level.games.models import Game
from next_level.guides.forms import GuideCategoryCreateForm, GuideCategoryEditForm, GuidePostCreateForm, \
    GuidePostEditForm
from next_level.guides.models import GuideCategory, GuidePost
from next_level.utils import UserOwnerMixin


class GuideCategoryListView(ListView):
    model = GuideCategory
    template_name = 'guides/guide-categories-list-page.html'

    def get_queryset(self):
        game = Game.objects.get(slug=self.kwargs['game_slug'])
        return self.model.objects.filter(to_game=game.id).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['add_url'] = reverse_lazy('guide category add', kwargs={
            'game_slug': self.kwargs['game_slug'],
        })

        return context


class GuideCategoryAddView(PermissionRequiredMixin, CreateView):
    template_name = 'base/form-page.html'
    model = GuideCategory
    form_class = GuideCategoryCreateForm
    permission_required = 'guides.add_guidecategory'

    def get_success_url(self):
        return reverse_lazy('guide category list', kwargs={
            'game_slug': self.object.to_game.slug,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['url'] = reverse_lazy('guide category add', kwargs={
            'game_slug': self.kwargs['game_slug'],
        })

        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.to_game = Game.objects.get(slug=self.kwargs['game_slug'])
        return super().form_valid(form)


class GuideSelectGameView(TemplateView):
    template_name = 'guides/guide-select-game-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        games = Game.objects.filter(status='Approved').order_by('-id')

        query = self.request.GET.get('title')

        if query:
            games = Game.objects.filter(title__icontains=query)

        context['search_form'] = SearchForm(self.request.GET or None)

        context['games'] = games

        return context


class GuideCategoryEditView(PermissionRequiredMixin, UpdateView):
    model = GuideCategory
    template_name = 'base/form-page.html'
    form_class = GuideCategoryEditForm
    permission_required = 'guides.change_guidecategory'

    def get_success_url(self):
        return reverse_lazy('guide category list', kwargs={
            'game_slug': self.object.to_game.slug,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['url'] = reverse_lazy('guide category edit', kwargs={
            'game_slug': self.object.to_game.slug,
            'slug': self.object.slug
        })

        context['button'] = 'Save Changes'

        return context


class GuideCategoryDeleteView(PermissionRequiredMixin, DeleteView):
    model = GuideCategory
    permission_required = 'guides.delete_guidecategory'

    def get(self, request, *args, **kwargs):
        success_url = reverse_lazy('guide category list', kwargs={
            'game_slug': self.kwargs['game_slug'],
        })

        guide_category = self.get_object()
        posts = guide_category.guidepost_set.all()

        for post in posts:
            post.guides_like_set.all().delete()

        posts.delete()
        guide_category.delete()

        return HttpResponseRedirect(success_url)


class GuidePostListView(ListView):
    model = GuidePost
    template_name = 'guides/guide-post-list-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['add_url'] = reverse_lazy('guide post add', kwargs={
            'game_slug': self.kwargs['game_slug'],
            'category_slug': self.kwargs['category_slug'],
        })

        return context

    def get_queryset(self):
        category = GuideCategory.objects.get(slug=self.kwargs['category_slug'])
        self.queryset = self.model.objects.filter(to_category=category.id).order_by('-id')

        return self.queryset


class GuidePostAddView(PermissionRequiredMixin, CreateView):
    template_name = 'base/form-page.html'
    model = GuidePost
    form_class = GuidePostCreateForm
    permission_required = 'guides.add_guidepost'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['url'] = reverse_lazy('guide post add', kwargs={
            'game_slug': self.kwargs['game_slug'],
            'category_slug': self.kwargs['category_slug'],
        })

        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.to_category = GuideCategory.objects.get(slug=self.kwargs['category_slug'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('guide posts list', kwargs={
            'game_slug': self.object.to_category.to_game.slug,
            'category_slug': self.object.to_category.slug,
        })


class GuidePostDetailsView(DetailView):
    template_name = 'guides/guide-post-details-page.html'
    model = GuidePost

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['post_is_liked_by_user'] = self.object.guides_like_set.filter(author_id=self.request.user.id)

        return context


class GuidePostEditView(PermissionRequiredMixin, UserOwnerMixin, UpdateView):
    template_name = 'base/form-page.html'
    model = GuidePost
    form_class = GuidePostEditForm
    success_url = reverse_lazy('index')
    permission_required = 'guides.change_guidepost'

    def get_success_url(self):
        return reverse_lazy('guide posts list', kwargs={
            'game_slug': self.kwargs['game_slug'],
            'category_slug': self.kwargs['category_slug'],
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['url'] = reverse_lazy('guide post edit', kwargs={
            'game_slug': self.kwargs['game_slug'],
            'category_slug': self.kwargs['category_slug'],
            'slug': self.object.slug
        })

        context['button'] = 'Save Changes'

        return context


class GuidePostDeleteView(PermissionRequiredMixin, UserOwnerMixin, DeleteView):
    model = GuidePost
    permission_required = 'guides.delete_guidepost'

    def get(self, request, *args, **kwargs):
        success_url = reverse_lazy('guide posts list', kwargs={
            'game_slug': self.kwargs['game_slug'],
            'category_slug': self.kwargs['category_slug'],
        })

        post = self.get_object()
        post.guides_like_set.all().delete()
        post.delete()

        return HttpResponseRedirect(success_url)
