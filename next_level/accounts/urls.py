from django.urls import path

from next_level.accounts.views import SignUpView

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
]
