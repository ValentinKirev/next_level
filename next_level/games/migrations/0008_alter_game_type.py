# Generated by Django 4.1.3 on 2022-12-14 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0007_alter_game_developer_alter_game_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='type',
            field=models.CharField(choices=[('Pay To Play', 'Pay To Play'), ('Free To Play', 'Free To Play'), ('Buy To Play', 'Buy To Play')], max_length=12),
        ),
    ]
