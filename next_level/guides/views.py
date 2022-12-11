from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from next_level.games.models import Game
from next_level.guides.forms import GuideCategoryCreateForm, GuideCategoryEditForm, GuidePostCreateForm, \
    GuidePostEditForm
from next_level.guides.models import GuideCategory, GuidePost


class GuideCategoryListView(ListView):
    model = GuideCategory
    template_name = 'guides/guide-categories-list-page.html'
    queryset = model.objects.all().order_by('-id')


class GuideCategoryAddView(CreateView):
    template_name = 'base/form-page.html'
    model = GuideCategory
    form_class = GuideCategoryCreateForm
    success_url = reverse_lazy('guide category list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['url'] = reverse_lazy('guide category add')

        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class GuideCategoryDetailsView(DetailView):
    model = GuideCategory
    template_name = 'guides/guide-category-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['games'] = Game.objects.all().order_by('-id')

        return context


class GuideCategoryEditView(UpdateView):
    model = GuideCategory
    template_name = 'base/form-page.html'
    form_class = GuideCategoryEditForm
    success_url = reverse_lazy('guide category list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['url'] = reverse_lazy('guide category edit', kwargs={
            'slug': self.object.slug
        })
        context['button'] = 'Save Changes'

        return context


class GuideCategoryDeleteView(DeleteView):
    model = GuideCategory
    success_url = reverse_lazy('guide category list')

    def get(self, request, *args, **kwargs):
        guide_category = self.get_object()
        guide_category.delete()

        return HttpResponseRedirect(self.success_url)


class GuidePostListView(ListView):
    model = GuidePost
    template_name = 'guides/guide-post-list-page.html'

    def get_queryset(self):
        category = GuideCategory.objects.get(slug=self.kwargs['category_slug'])
        game = Game.objects.get(slug=self.kwargs['game_slug'])
        self.queryset = self.model.objects.filter(to_game=game.id, to_category=category.id).order_by('-id')

        return self.queryset


class GuidePostAddView(CreateView):
    template_name = 'base/form-page.html'
    model = GuidePost
    form_class = GuidePostCreateForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['url'] = reverse_lazy('guide post add')

        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class GuidePostEditView(UpdateView):
    template_name = 'base/form-page.html'
    model = GuidePost
    form_class = GuidePostEditForm
    success_url = reverse_lazy('index')
    # def get_success_url(self):
    #     return reverse_lazy('news details', kwargs={
    #         'slug': self.object.slug
    #     })

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['url'] = reverse_lazy('guide post edit', kwargs={
            'slug': self.object.slug
        })
        context['button'] = 'Save Changes'

        return context


class GuidePostDeleteView(DeleteView):
    model = GuidePost
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        self.get_object().delete()

        return HttpResponseRedirect(self.success_url)
