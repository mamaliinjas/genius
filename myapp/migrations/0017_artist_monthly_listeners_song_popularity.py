# Generated by Django 5.1.4 on 2024-12-30 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_remove_song_audio_file_artist_spotify_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='monthly_listeners',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='popularity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
