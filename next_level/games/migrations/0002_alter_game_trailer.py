# Generated by Django 4.1.3 on 2022-12-09 12:01

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='trailer',
            field=embed_video.fields.EmbedVideoField(),
        ),
    ]
