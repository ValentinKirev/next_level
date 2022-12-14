from django.contrib.auth.decorators import login_required
from django.urls import path

from next_level.guides.views import GuideCategoryAddView, GuideCategoryListView, GuideCategoryEditView, \
    GuideCategoryDeleteView, GuideSelectGameView, GuidePostAddView, GuidePostEditView, GuidePostDeleteView, \
    GuidePostListView, GuidePostDetailsView

urlpatterns = [
    path('', GuideSelectGameView.as_view(), name='guide select view'),
    path('<slug:game_slug>/categories/', GuideCategoryListView.as_view(), name='guide category list'),
    path('<slug:game_slug>/categories/add/', login_required(GuideCategoryAddView.as_view()), name='guide category add'),
    path('<slug:game_slug>/categories/edit/<slug:slug>/', login_required(GuideCategoryEditView.as_view()),
         name='guide category edit'),
    path('<slug:game_slug>/categories/delete/<slug:slug>/', login_required(GuideCategoryDeleteView.as_view()),
         name='guide category delete'),
    path('<slug:game_slug>/categories/<slug:category_slug>/posts/', GuidePostListView.as_view(),
         name='guide posts list'),
    path('<slug:game_slug>/categories/<slug:category_slug>/posts/add/', login_required(GuidePostAddView.as_view()),
         name='guide post add'),
    path('<slug:game_slug>/categories/<slug:category_slug>/posts/details/<slug:slug>/', GuidePostDetailsView.as_view(),
         name='guide post details'),
    path('<slug:game_slug>/categories/<slug:category_slug>/posts/edit/<slug:slug>/', login_required(GuidePostEditView.as_view()),
         name='guide post edit'),
    path('<slug:game_slug>/categories/<slug:category_slug>/posts/delete/<slug:slug>/', login_required(GuidePostDeleteView.as_view()),
         name='guide post delete'),
]
