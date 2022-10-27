# Generated by Django 4.1.1 on 2022-09-22 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0008_rename_reviewer_review_review_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='avg_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='number_of_ratings',
            field=models.IntegerField(default=0),
        ),
    ]
