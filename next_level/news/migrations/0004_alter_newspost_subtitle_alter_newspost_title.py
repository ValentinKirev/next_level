# Generated by Django 4.1.3 on 2022-12-05 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_rename_media_newspost_image_newspost_link_to_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspost',
            name='subtitle',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='newspost',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
