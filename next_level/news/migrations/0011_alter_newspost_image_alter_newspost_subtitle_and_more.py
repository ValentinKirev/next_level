# Generated by Django 4.1.3 on 2022-12-13 11:31

import django.core.validators
from django.db import migrations, models
import next_level.validators


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_newspost_updated_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspost',
            name='image',
            field=models.FileField(upload_to='news_post', validators=[next_level.validators.validate_image_sile_less_than_5mb]),
        ),
        migrations.AlterField(
            model_name='newspost',
            name='subtitle',
            field=models.CharField(blank=True, max_length=200, null=True, validators=[next_level.validators.validate_all_characters_is_alphanumeric, django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='newspost',
            name='title',
            field=models.CharField(max_length=200, unique=True, validators=[next_level.validators.validate_all_characters_is_alphanumeric, django.core.validators.MinLengthValidator(2)]),
        ),
    ]
