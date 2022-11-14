from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class NewsPost(models.Model):
    MAX_TITLE_LENGTH = 100
    MAX_SUBTITLE_LENGTH = 100

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH,
        null=False,
        blank=False
    )

    subtitle = models.CharField(
        max_length=MAX_SUBTITLE_LENGTH,
        null=True,
        blank=True
    )

    # author = models.CharField(
    #     max_length=30,
    #     null=False,
    #     blank=True
    # )

    publication_date_and_time = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=True
    )

    description = models.TextField(
        null=False,
        blank=True
    )

    media = models.FileField(
        upload_to='news_post',
        null=False,
        blank=True
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.id}")

        return super().save(*args, **kwargs)
