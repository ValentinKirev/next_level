from django.contrib.auth.decorators import login_required
from django.urls import path

from next_level.common.views import CommentAddView, CommentEditView, CommentDeleteView, LikeView, RateView, IndexView, \
    AboutView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('comments/<slug:slug>/', login_required(CommentAddView.as_view()), name='comment add'),
    path('comments/<slug:slug>/edit/<int:pk>', login_required(CommentEditView.as_view()), name='comment edit'),
    path('comments/<slug:slug>/delete/<int:pk>', login_required(CommentDeleteView.as_view()), name='comment delete'),
    path('like/<slug:slug>/', login_required(LikeView.as_view()), name='like'),
    path('rate/<slug:slug>/', login_required(RateView.as_view()), name='rate'),
    path('about/', AboutView.as_view(), name='about'),
]
