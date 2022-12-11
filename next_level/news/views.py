from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from next_level.common.forms import CommentCreateForm, SearchForm
from next_level.news.forms import NewsCreateForm, NewsEditForm
from next_level.news.models import NewsPost


class NewsList(ListView):
    model = NewsPost
    template_name = 'news/news-list-page.html'
    paginate_by = 3
    queryset = model.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['search_form'] = SearchForm(self.request.GET or None)

        return context

    def get_queryset(self):
        query = self.request.GET.get('title')

        if query:
            self.queryset = self.model.objects.filter(title__icontains=query)

        return self.queryset


class NewsAddView(CreateView):
    template_name = 'base/form-page.html'
    model = NewsPost
    form_class = NewsCreateForm
    success_url = reverse_lazy('news list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['media'] = True
        context['url'] = reverse_lazy('news add')

        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NewsDetailsView(DetailView):
    template_name = 'news/news-details-page.html'
    model = NewsPost

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['post_is_liked_by_user'] = self.object.like_set.filter(author_id=self.request.user.id)
        context['form'] = CommentCreateForm()

        return context


class NewsEditView(UpdateView):
    template_name = 'base/form-page.html'
    model = NewsPost
    form_class = NewsEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['media'] = True
        context['url'] = reverse_lazy('news edit', kwargs={
            'slug': self.object.slug
        })
        context['button'] = 'Save Changes'

        return context

    def get_success_url(self):
        return reverse_lazy('news details', kwargs={
            'slug': self.object.slug
        })


class NewsDeleteView(DeleteView):
    model = NewsPost
    success_url = reverse_lazy('news list')

    def get(self, request, *args, **kwargs):
        news_post = self.get_object()
        news_post.comment_set.all().delete()
        news_post.like_set.all().delete()
        news_post.delete()

        return HttpResponseRedirect(self.success_url)
