# Generated by Django 3.2 on 2023-07-26 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_alter_movie_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='url',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
