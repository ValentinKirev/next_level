from django.urls import path

from next_level.common.views import CommentAddView, CommentEditView, CommentDeleteView, LikeView, RateView

urlpatterns = [
    path('comments/<str:slug>/', CommentAddView.as_view(), name='comment add'),
    path('comments/<str:slug>/edit/<int:pk>', CommentEditView.as_view(), name='comment edit'),
    path('comments/<str:slug>/delete/<int:pk>', CommentDeleteView.as_view(), name='comment delete'),
    path('like/<str:slug>/', LikeView.as_view(), name='like'),
    path('rate/<str:slug>/', RateView.as_view(), name='rate'),
]
