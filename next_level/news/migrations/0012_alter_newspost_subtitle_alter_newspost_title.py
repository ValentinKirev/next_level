# Generated by Django 4.1.3 on 2022-12-14 16:49

import django.core.validators
from django.db import migrations, models
import next_level.validators


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_alter_newspost_image_alter_newspost_subtitle_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspost',
            name='subtitle',
            field=models.CharField(blank=True, max_length=200, null=True, validators=[next_level.validators.validate_post_title_contains_only_allowed_characters, django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='newspost',
            name='title',
            field=models.CharField(max_length=200, unique=True, validators=[next_level.validators.validate_post_title_contains_only_allowed_characters, django.core.validators.MinLengthValidator(2)]),
        ),
    ]
