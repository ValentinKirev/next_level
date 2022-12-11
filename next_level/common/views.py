from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from next_level.common.forms import CommentCreateForm, CommentEditForm, SearchForm
from next_level.common.models import Comment, Like, Rating
from next_level.games.models import Game
from next_level.news.models import NewsPost


class IndexView(ListView):
    model = NewsPost
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['news'] = NewsPost.objects.all().order_by('-id')[:3]

        return context


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
    template_name = 'base/form-page.html'
    model = Comment
    form_class = CommentEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['post'] = NewsPost.objects.get(pk=self.object.to_news_post_id)
        context['button'] = 'Save Changes'
        context['url'] = reverse_lazy('comment edit', kwargs={
            'slug': self.kwargs['slug'], 'pk': self.get_object().pk
        })

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


class RateView(View):

    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = body_unicode.split('&')

        game = Game.objects.get(slug=self.kwargs['slug'])
        Rating.objects.filter(game=game, user=request.user).delete()
        game.rating_set.create(user=request.user, rating=int(body[0][-1]))
        game.average_rating = sum(rating.rating for rating in game.rating_set.all()) / game.rating_set.count() \
            if game.rating_set.count() > 0 else 0
        game.save()
        success_url = reverse_lazy('game details', kwargs={
            'slug': game.slug
        })

        return HttpResponseRedirect(success_url)
