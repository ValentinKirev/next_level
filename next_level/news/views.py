from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from next_level.common.forms import CommentCreateForm, SearchForm
from next_level.news.forms import NewsCreateForm, NewsEditForm
from next_level.news.models import NewsPost


class IndexView(ListView):
    model = NewsPost
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['news'] = NewsPost.objects.all().order_by('-id')[:3]

        return context


class NewsList(ListView):
    model = NewsPost
    template_name = 'news/news-list-page.html'
    paginate_by = 3
    queryset = NewsPost.objects.all().order_by('-id')
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = self.form_class()

        return context

    def get_queryset(self):
        query = self.request.GET.get('title')
        if query:
            object_list = self.model.objects.filter(title__icontains=query)
        else:
            object_list = self.queryset
        return object_list


class NewsAddView(CreateView):
    template_name = 'news/news-add-page.html'
    model = NewsPost
    form_class = NewsCreateForm
    success_url = reverse_lazy('news list')

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
    template_name = 'news/news-edit-page.html'
    model = NewsPost
    form_class = NewsEditForm

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
