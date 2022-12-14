from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.text import slugify

from next_level.games.models import Game
from next_level.validators import validate_image_sile_less_than_5mb, \
    validate_post_title_contains_only_allowed_characters

UserModel = get_user_model()


class GuideCategory(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    MAX_TITLE_LENGTH = 50

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH,
        validators=(
            validate_post_title_contains_only_allowed_characters,
            MinLengthValidator(2)
        ),
        null=False,
        blank=False
    )

    description = models.TextField(
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

    author = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT
    )

    to_game = models.ForeignKey(
        Game,
        on_delete=models.RESTRICT
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=False,
        blank=True
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.id}")

        return super().save(*args, **kwargs)


class GuidePost(models.Model):
    MAX_TITLE_LENGTH = 50

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH,
        validators=(
            validate_post_title_contains_only_allowed_characters,
            MinLengthValidator(2)
        ),
        null=False,
        blank=False
    )

    description = models.TextField(
        null=False,
        blank=False
    )

    image = models.ImageField(
        upload_to='guides',
        validators=(
            validate_image_sile_less_than_5mb,
        ),
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

    author = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT
    )

    to_category = models.ForeignKey(
        GuideCategory,
        on_delete=models.RESTRICT
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=False,
        blank=True
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f"{self.title}{self.id}")

        return super().save(*args, **kwargs)
