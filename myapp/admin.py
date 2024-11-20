from django.contrib import admin
from .models import Artist, Album, Song

# Register your models here.
class ArtistAdmin(admin.ModelAdmin):
    search_fields = ['name', 'bio']
    list_display = ['name', 'bio', 'profile_picture']
    list_filter = ['name']

class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['title', 'artist__name']
    list_display = ['title', 'release_date', 'artist']
    list_filter = ['release_date', 'artist']

class SongAdmin(admin.ModelAdmin):
    search_fields = ['title', 'artist__name']
    list_display = ['title', 'duration', 'artist']
    list_filter = ['artist']


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)