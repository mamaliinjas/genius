# Generated by Django 5.1.3 on 2024-11-26 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_album_genre_album_views_artist_genre_artist_views_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='cover_photo',
            field=models.ImageField(blank=True, null=True, upload_to='song_covers/'),
        ),
    ]
