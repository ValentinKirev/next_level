from django.urls import path

from next_level.guides.views import GuideCategoryAddView, GuideCategoryListView, GuideCategoryEditView, \
    GuideCategoryDeleteView, GuideSelectGameView, GuidePostAddView, GuidePostEditView, GuidePostDeleteView, \
    GuidePostListView, GuidePostDetailsView

urlpatterns = [
    path('', GuideSelectGameView.as_view(), name='guide select view'),
    path('<slug:game_slug>/categories/', GuideCategoryListView.as_view(), name='guide category list'),
    path('<slug:game_slug>/categories/add/', GuideCategoryAddView.as_view(), name='guide category add'),
    path('<slug:game_slug>/categories/edit/<slug:slug>/', GuideCategoryEditView.as_view(),
         name='guide category edit'),
    path('<slug:game_slug>/categories/delete/<slug:slug>/', GuideCategoryDeleteView.as_view(),
         name='guide category delete'),
    path('<slug:game_slug>/categories/<slug:category_slug>/posts/', GuidePostListView.as_view(),
         name='guide posts list'),
    path('<slug:game_slug>/categories/<slug:category_slug>/posts/add/', GuidePostAddView.as_view(),
         name='guide post add'),
    path('<slug:game_slug>/categories/<slug:category_slug>/posts/details/<slug:slug>/', GuidePostDetailsView.as_view(),
         name='guide post details'),
    path('<slug:game_slug>/categories/<slug:category_slug>/posts/edit/<slug:slug>/', GuidePostEditView.as_view(),
         name='guide post edit'),
    path('<slug:game_slug>/categories/<slug:category_slug>/posts/delete/<slug:slug>/', GuidePostDeleteView.as_view(),
         name='guide post delete'),
]
