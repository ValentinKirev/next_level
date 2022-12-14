from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, TemplateView

from next_level.common.forms import CommentCreateForm, CommentEditForm
from next_level.common.models import Comment, Like, Rating
from next_level.games.models import Game
from next_level.guides.models import GuidePost
from next_level.news.models import NewsPost
from next_level.utils import UserOwnerMixin

UserModel = get_user_model()


class IndexView(ListView):
    model = NewsPost
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['news'] = NewsPost.objects.all().order_by('-id')[:3]

        return context


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        try:
            context['developer'] = UserModel.objects.get(pk=111)
        except ObjectDoesNotExist:
            raise Http404

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

        try:
            form.instance.to_news_post = NewsPost.objects.get(slug=self.kwargs['slug'])
        except ObjectDoesNotExist:
            raise Http404

        return super().form_valid(form)


class CommentEditView(UserOwnerMixin, UpdateView):
    template_name = 'base/form-page.html'
    model = Comment
    form_class = CommentEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        try:
            context['post'] = NewsPost.objects.get(pk=self.object.to_news_post_id)
        except ObjectDoesNotExist:
            raise Http404

        context['button'] = 'Save Changes'
        context['url'] = reverse_lazy('comment edit', kwargs={
            'slug': self.kwargs['slug'], 'pk': self.get_object().pk
        })

        return context

    def get_success_url(self):
        return reverse_lazy('news details', kwargs={
            'slug': self.kwargs['slug'],
        })


class CommentDeleteView(UserOwnerMixin, DeleteView):
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

    def get(self, request, *args, **kwargs):
        news_post = None
        liked_news_post = None
        guide_post = None
        liked_guide_post = None

        try:
            news_post = NewsPost.objects.get(slug=self.kwargs['slug'])
            liked_news_post = Like.objects.filter(to_news_post_id=news_post.id, author=request.user) \
                .first()
        except ObjectDoesNotExist:
            guide_post = GuidePost.objects.get(slug=self.kwargs['slug'])
            liked_guide_post = Like.objects.filter(to_guide_post=guide_post.id, author=request.user) \
                .first()

        if news_post is not None:
            if liked_news_post:
                liked_news_post.delete()
            else:
                like = Like(to_news_post=news_post, author=request.user)
                like.save()
            success_url = reverse_lazy('news details', kwargs={
                'slug': self.kwargs['slug'],
            })
        else:
            if liked_guide_post:
                liked_guide_post.delete()
            else:
                like = Like(to_guide_post=guide_post, author=request.user)
                like.save()
            success_url = reverse_lazy('guide post details', kwargs={
                'game_slug': guide_post.to_category.to_game.slug,
                'category_slug': guide_post.to_category.slug,
                'slug': self.kwargs['slug'],
            })

        return HttpResponseRedirect(success_url)


class RateView(View):

    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = body_unicode.split('&')

        try:
            game = Game.objects.get(slug=self.kwargs['slug'])
        except ObjectDoesNotExist:
            raise Http404

        Rating.objects.filter(game=game, user=request.user).delete()
        game.rating_set.create(user=request.user, rating=int(body[0][-1]))
        game.average_rating = sum(rating.rating for rating in game.rating_set.all()) / game.rating_set.count() \
            if game.rating_set.count() > 0 else 0
        game.save()
        success_url = reverse_lazy('game details', kwargs={
            'slug': game.slug
        })

        return HttpResponseRedirect(success_url)
