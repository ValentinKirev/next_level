from django.urls import path

from next_level.common.views import CommentAddView, CommentEditView, CommentDeleteView, LikeView, RateView, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('comments/<slug:slug>/', CommentAddView.as_view(), name='comment add'),
    path('comments/<slug:slug>/edit/<int:pk>', CommentEditView.as_view(), name='comment edit'),
    path('comments/<slug:slug>/delete/<int:pk>', CommentDeleteView.as_view(), name='comment delete'),
    path('like/<slug:slug>/', LikeView.as_view(), name='like'),
    path('rate/<slug:slug>/', RateView.as_view(), name='rate'),
]
