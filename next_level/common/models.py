from django.contrib.auth import get_user_model
from django.db import models

from next_level.games.models import Game
from next_level.guides.models import GuidePost
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

    updated_on = models.DateTimeField(
        auto_now=True,
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

    def __str__(self):
        return self.text


class Like(models.Model):
    to_news_post = models.ForeignKey(
        NewsPost,
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )

    to_guide_post = models.ForeignKey(
        GuidePost,
        on_delete=models.RESTRICT,
        related_name='guides_like_set',
        null=True,
        blank=True
    )

    author = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT
    )

    def __str__(self):
        result = f"ID={self.id} author={self.author} "
        result += f"to_guide_post={self.to_guide_post}" if self.to_guide_post else f"to_news_post={self.to_news_post}"

        return result


class Rating(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.RESTRICT
    )

    rating = models.IntegerField(
        default=0,
        null=False,
        blank=False
    )

    def __str__(self):
        return f"ID={self.id} author={self.user} to_game={self.game}"
