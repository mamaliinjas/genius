# Generated by Django 5.1.4 on 2025-01-14 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0022_alter_artist_monthly_listeners_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='total_views',
            field=models.IntegerField(default=0),
        ),
    ]
