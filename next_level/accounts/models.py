from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django_countries.data import COUNTRIES

from next_level.accounts.managers import AppUserManager
from next_level.accounts.validators import validate_username_contains_allowed_characters, \
    validate_names_contain_only_letters, validate_image_sile_less_than_5mb


class AppUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'User'

    MAX_USERNAME_LENGTH = 50
    MIN_USERNAME_LENGTH = 3

    username = models.CharField(
        max_length=MAX_USERNAME_LENGTH,
        unique=True,
        validators=(
            MinLengthValidator(MIN_USERNAME_LENGTH),
            validate_username_contains_allowed_characters
        ),
        null=False,
        blank=False
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False
    )

    is_superuser = models.BooleanField(
        default=False,
        null=False,
        blank=False
    )

    is_staff = models.BooleanField(
        default=False,
        null=False,
        blank=False
    )

    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False
    )

    date_joined = models.DateTimeField(
        auto_now_add=True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = AppUserManager()


class Profile(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'

    GENDER_CHOICES = [
        (MALE, MALE),
        (FEMALE, FEMALE),
    ]

    MAX_FIRST_NAME_LENGTH = 25
    MAX_LAST_NAME_LENGTH = 25
    MIN_FIRST_NAME_LENGTH = 2
    MIN_LAST_NAME_LENGTH = 2
    MAX_CITY_LENGTH = 30
    MAX_GENDER_LENGTH = max(len(value) for (_, value) in GENDER_CHOICES)
    MAX_COUNTRY_LENGTH = max(len(value) for (_, value) in COUNTRIES.items())

    first_name = models.CharField(
        max_length=MAX_FIRST_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_FIRST_NAME_LENGTH),
            validate_names_contain_only_letters,
        ),
        null=True,
        blank=True
    )

    last_name = models.CharField(
        max_length=MAX_LAST_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_LAST_NAME_LENGTH),
            validate_names_contain_only_letters,
        ),
        null=True,
        blank=True
    )

    age = models.PositiveIntegerField(
        validators=(
            MinValueValidator(12),
        ),
        null=True,
        blank=True
    )

    gender = models.CharField(
        max_length=MAX_GENDER_LENGTH,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )

    country = models.CharField(
        max_length=MAX_COUNTRY_LENGTH,
        choices=sorted(COUNTRIES.items()),
        null=True,
        blank=True
    )

    city = models.CharField(
        max_length=MAX_CITY_LENGTH,
        null=True,
        blank=True
    )

    description = models.TextField(
        null=True,
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to='profiles',
        validators=(
            validate_image_sile_less_than_5mb,
        ),
        null=True,
        blank=True
    )

    user = models.OneToOneField(
        AppUser, on_delete=models.CASCADE
    )

    @property
    def get_full_name(self):
        if self.first_name is not None and self.last_name is not None:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name is not None:
            return self.first_name
        elif self.last_name is not None:
            return self.last_name
