from django.contrib import admin
from .models import Artist, Album, Song , News

# Register your models here.
class ArtistAdmin(admin.ModelAdmin):
    search_fields = ['name', 'bio' , 'aka']
    list_display = ['name', 'bio', 'profile_picture' , 'aka']
    list_filter = ['name']

class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['title', 'artist__name']
    list_display = ['title', 'release_date', 'artist']
    list_filter = ['release_date', 'artist']

class SongAdmin(admin.ModelAdmin):
    search_fields = ['title', 'artist__name']
    list_display = ['title', 'duration', 'artist']
    list_filter = ['artist']
    
class NewsAdmin(admin.ModelAdmin):
    list_display=['title' , 'is_featured' , 'published_date']
    list_filter=['published_date' , 'is_featured']
    search_fields=['title']
    


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(News , NewsAdmin)