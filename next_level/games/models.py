from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.text import slugify
from embed_video.fields import EmbedVideoField

from next_level.validators import validate_all_characters_is_alphanumeric, validate_image_sile_less_than_5mb

UserModel = get_user_model()


class Game(models.Model):
    MAX_NAME_LENGTH = 50
    MAX_DEVELOPER_LENGTH = 50

    PAY_TO_PLAY = "Pay To Play"
    FREE_TO_PLAY = "Free To Play"
    BUY_TO_PLAY = "Buy To Play"

    TYPE_CHOICES = [
        (PAY_TO_PLAY, PAY_TO_PLAY),
        (FREE_TO_PLAY, FREE_TO_PLAY),
        (BUY_TO_PLAY, BUY_TO_PLAY),
    ]

    MAX_TYPE_CHOICES_LENGTH = max(len(value) for (_, value) in TYPE_CHOICES)

    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

    STATUS_CHOICES = [
        (PENDING, PENDING),
        (APPROVED, APPROVED),
        (REJECTED, REJECTED)
    ]

    MAX_STATUS_CHOICES_LENGTH = max(len(value) for (_, value) in STATUS_CHOICES)

    title = models.CharField(
        max_length=MAX_NAME_LENGTH,
        unique=True,
        validators=(
            validate_all_characters_is_alphanumeric,
            MinLengthValidator(2)
        ),
        null=False,
        blank=False
    )

    description = models.TextField(
        null=False,
        blank=False
    )

    image = models.FileField(
        upload_to='games',
        validators=(
            validate_image_sile_less_than_5mb,
        ),
        null=False,
        blank=False,
    )

    developer = models.CharField(
        max_length=MAX_DEVELOPER_LENGTH,
        validators=(
            MinLengthValidator(2),
        ),
        null=False,
        blank=False
    )

    release_date = models.DateField(
        null=False,
        blank=False
    )

    max_level = models.PositiveIntegerField(
        null=False,
        blank=False
    )

    official_website = models.URLField(
        null=False,
        blank=False
    )

    trailer = EmbedVideoField(
        null=False,
        blank=False
    )

    type = models.CharField(
        max_length=MAX_TYPE_CHOICES_LENGTH,
        choices=TYPE_CHOICES,
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

    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=False,
        blank=True
    )

    author = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=MAX_STATUS_CHOICES_LENGTH,
        choices=STATUS_CHOICES,
        default=PENDING,
        null=False,
        blank=False
    )

    average_rating = models.FloatField(
        default=0,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.id}")

        return super().save(*args, **kwargs)
