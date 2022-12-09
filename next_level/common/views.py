from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from next_level.common.forms import CommentCreateForm, CommentEditForm
from next_level.common.models import Comment, Like
from next_level.news.models import NewsPost


class CommentAddView(CreateView):
    model = Comment
    form_class = CommentCreateForm

    def get_success_url(self):
        return reverse_lazy('news details', kwargs={
            'slug': self.kwargs['slug'],
        })

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.to_news_post = NewsPost.objects.get(slug=self.kwargs['slug'])
        return super().form_valid(form)


class CommentEditView(UpdateView):
    template_name = 'common/comment-edit-page.html'
    model = Comment
    form_class = CommentEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['post'] = NewsPost.objects.get(pk=self.object.to_news_post_id)
        return context

    def get_success_url(self):
        return reverse_lazy('news details', kwargs={
            'slug': self.kwargs['slug'],
        })


class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse_lazy('news details', kwargs={
            'slug': self.kwargs['slug'],
        })

    def get(self, request, *args, **kwargs):
        self.get_object().delete()
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)


class LikeView(View):
    model = Like

    def get_success_url(self):
        return reverse_lazy('news details', kwargs={
            'slug': self.kwargs['slug'],
        })

    def get(self, request, *args, **kwargs):

        news_post = NewsPost.objects.get(slug=self.kwargs['slug'])
        liked_object = Like.objects.filter(to_news_post_id=news_post.id, author=request.user) \
            .first()

        if liked_object:
            liked_object.delete()
        else:
            like = Like(to_news_post=news_post, author=request.user)
            like.save()

        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)
