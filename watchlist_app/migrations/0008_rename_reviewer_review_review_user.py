# Generated by Django 4.1.1 on 2022-09-22 04:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0007_review_reviewer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='reviewer',
            new_name='review_user',
        ),
    ]
