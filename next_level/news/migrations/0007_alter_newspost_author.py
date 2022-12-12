# Generated by Django 4.1.3 on 2022-12-09 07:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0006_alter_newspost_description_alter_newspost_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspost',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
    ]