# Generated by Django 5.1.4 on 2024-12-30 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_alter_artist_monthly_listeners'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='popularity',
        ),
        migrations.RemoveField(
            model_name='song',
            name='spotify_id',
        ),
    ]
