# Generated by Django 4.1.3 on 2022-12-05 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_alter_newspost_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspost',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='newspost',
            name='image',
            field=models.FileField(upload_to='news_post'),
        ),
    ]
