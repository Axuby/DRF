# Generated by Django 4.1.1 on 2022-09-26 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0013_rename_platform_watchlist_watchlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='watchlist',
            new_name='platform',
        ),
    ]
