# Generated by Django 4.1.3 on 2022-11-18 15:16

import django.core.validators
from django.db import migrations, models
import next_level.accounts.validators


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='username',
            field=models.CharField(max_length=50, unique=True, validators=[django.core.validators.MinLengthValidator(3), next_level.accounts.validators.validate_username_contains_allowed_characters]),
        ),
    ]
