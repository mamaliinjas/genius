# Generated by Django 5.1.4 on 2025-01-03 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_remove_lyricline_timestamp_remove_song_lyrics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='monthly_listeners',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='spotify_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
