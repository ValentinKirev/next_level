from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, TemplateView

from next_level.accounts.forms import UserCreateForm, UserLoginForm, ProfileEditForm
from next_level.accounts.models import Profile
from next_level.utils import UserOwnerMixin

UserModel = get_user_model()


class SignUpView(CreateView):
    template_name = 'accounts/register-page.html'
    model = UserModel
    form_class = UserCreateForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('index'))
        else:
            form = self.form_class()
            return render(request, self.template_name, {'form': form})

    def get_success_url(self):
        return reverse_lazy('profile edit', kwargs={
            'pk': self.object.profile.id
        })

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        group = Group.objects.get(name='User')
        user.groups.add(group)
        login(self.request, user)
        self.object = user

        return HttpResponseRedirect(self.get_success_url())


class SignInView(LoginView):
    template_name = 'accounts/login-page.html'
    form_class = UserLoginForm


class SignOutView(LogoutView):
    pass


class ProfileDetailsView(DetailView):
    model = Profile
    template_name = 'accounts/profile-details-page.html'


class ProfileEditView(PermissionRequiredMixin, UserOwnerMixin, UpdateView):
    template_name = 'accounts/profile-edit-page.html'
    model = Profile
    form_class = ProfileEditForm
    permission_required = 'accounts.change_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        if self.request.META.get('HTTP_REFERER', 0) and \
                self.request.META['HTTP_REFERER'] == self.request.build_absolute_uri(reverse_lazy('register')):
            context['created'] = True

        return context

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={
            'pk': self.object.id
        })


class ProfileDeleteView(PermissionRequiredMixin, UserOwnerMixin, DeleteView):
    model = Profile
    success_url = reverse_lazy('profile successfully deleted')
    permission_required = 'accounts.delete_profile'

    def get(self, request, *args, **kwargs):
        user = self.get_object().user
        news_posts = user.newspost_set.all()

        for news_post in news_posts:
            news_post.comment_set.all().delete()
            news_post.like_set.all().delete()

        news_posts.delete()

        games = user.game_set.all()

        for game in games:
            categories = game.guidecategory_set.all()

            for category in categories:
                posts = category.guidepost_set.all()

                for post in posts:
                    post.guides_like_set.all().delete()

                posts.delete()

            categories.delete()

        user_categories = user.guidecategory_set.all()

        for category in user_categories:
            posts = category.guidepost_set.all()

            for post in posts:
                post.guides_like_set.all().delete()

            posts.delete()

        user_guides = user.guidepost_set.all()

        for guide in user_guides:
            guide.guides_like_set.all().delete()

        user_categories.delete()
        user_guides.delete()
        user.like_set.all().delete()
        user.profile.delete()
        user.delete()

        return HttpResponseRedirect(self.success_url)


class ProfileSuccessfullyDeleted(TemplateView):
    template_name = 'accounts/profile-deleted-page.html'
