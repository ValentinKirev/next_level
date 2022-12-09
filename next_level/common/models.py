from django.contrib.auth import get_user_model
from django.db import models

from next_level.news.models import NewsPost

UserModel = get_user_model()


class Comment(models.Model):
    class Meta:
        ordering = ['-publication_date_and_time']

    text = models.TextField(
        null=False,
        blank=False
    )

    publication_date_and_time = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=True
    )

    to_news_post = models.ForeignKey(
        NewsPost,
        on_delete=models.RESTRICT
    )

    author = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT
    )


class Like(models.Model):
    to_news_post = models.ForeignKey(
        NewsPost,
        on_delete=models.RESTRICT
    )

    author = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT
    )
