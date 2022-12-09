from django.urls import path

from next_level.accounts.views import SignUpView, SignInView, SignOutView, ProfileEditView, ProfileDetailsView, \
    ProfileDeleteView, ProfileSuccessfullyDeleted

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('profile/details/<int:pk>', ProfileDetailsView.as_view(), name='profile details'),
    path('profile/edit/<int:pk>', ProfileEditView.as_view(), name='profile edit'),
    path('profile/delete/<int:pk>', ProfileDeleteView.as_view(), name='profile delete'),
    path('profile/deleted/', ProfileSuccessfullyDeleted.as_view(), name='profile successfully deleted'),
]

from .signals import *
