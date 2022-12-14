# Generated by Django 4.1.3 on 2022-12-14 15:56

from django.db import migrations, models
import next_level.validators


class Migration(migrations.Migration):

    dependencies = [
        ('guides', '0008_alter_guidecategory_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='guidepost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='guides', validators=[next_level.validators.validate_image_sile_less_than_5mb]),
        ),
    ]
