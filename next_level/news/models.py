from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from embed_video.fields import EmbedVideoField

UserModel = get_user_model()


class NewsPost(models.Model):
    MAX_TITLE_LENGTH = 200
    MAX_SUBTITLE_LENGTH = 200

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH,
        unique=True,
        null=False,
        blank=False
    )

    subtitle = models.CharField(
        max_length=MAX_SUBTITLE_LENGTH,
        null=True,
        blank=True
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

    description = models.TextField(
        null=False,
        blank=False
    )

    image = models.FileField(
        upload_to='news_post',
        null=False,
        blank=False,
    )

    link_to_video = EmbedVideoField(
        null=True,
        blank=True
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=False,
        blank=True
    )

    author = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.id}")

        return super().save(*args, **kwargs)
