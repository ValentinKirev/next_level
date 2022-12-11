from django.urls import path, include

from next_level.guides.views import GuideCategoryAddView, GuideCategoryListView, GuideCategoryEditView, \
    GuideCategoryDeleteView, GuideCategoryDetailsView, GuidePostAddView, GuidePostEditView, GuidePostDeleteView, \
    GuidePostListView

urlpatterns = [
    path('categories/', include([
        path('', GuideCategoryListView.as_view(), name='guide category list'),
        path('add/', GuideCategoryAddView.as_view(), name='guide category add'),
        path('details/<slug:slug>/', GuideCategoryDetailsView.as_view(), name='guide category details'),
        path('edit/<slug:slug>/', GuideCategoryEditView.as_view(), name='guide category edit'),
        path('delete/<slug:slug>/', GuideCategoryDeleteView.as_view(), name='guide category delete'),
    ])),
    path('posts/', include([
        path('add/', GuidePostAddView.as_view(), name='guide post add'),
        path('edit/<slug:slug>/', GuidePostEditView.as_view(), name='guide post edit'),
        path('delete/<slug:slug>/', GuidePostDeleteView.as_view(), name='guide post delete'),
    ])),
    path('categories/<slug:category_slug>/<slug:game_slug>/posts/', GuidePostListView.as_view(), name='guide posts list'),
]
