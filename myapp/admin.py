from django.contrib import admin
from .models import Artist, Album, Song , News , Video , LyricLine
from myapp.spotify import update_spotify_views
# Register your models here.
def update_spotify_data(modeladmin, request, queryset):
    # Call the function that updates all artist and song views
    update_spotify_views()



class ArtistAdmin(admin.ModelAdmin):
    search_fields = ['name', 'bio', 'aka', 'twitter','spotify_id' , 'soundcloud', 'spotify', 'instagram' , 'telegram' , 'youtube']
    list_display = ['name', 'bio', 'profile_picture', 'aka' ,'spotify_id' ,'get_monthly_listeners', 'twitter', 'instagram', 'soundcloud', 'spotify' , 'telegram' , 'youtube']
    list_filter = ['name']
    actions = [update_spotify_data]

class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['title', 'artist__name']
    list_display = ['title', 'release_date', 'artist']
    list_filter = ['release_date', 'artist']

class SongAdmin(admin.ModelAdmin):
    search_fields = ['title', 'artist__name']
    list_display = ['title', 'duration', 'artist' ]
    list_filter = ['artist']    
class NewsAdmin(admin.ModelAdmin):
    list_display=['title' , 'is_featured' , 'published_date']
    list_filter=['published_date' , 'is_featured']
    search_fields=['title']
    
class VideoAdmin(admin.ModelAdmin):
    list_display=['title' , 'description' , 'created_at' ]
    list_filter=['title' , 'embed_code' , 'created_at']
    search_fields=['title']
    
class LyricLineAdmin(admin.ModelAdmin):
    list_display = ('song', 'line_text', 'timestamp', 'meaning')
    list_filter = ('song',)
    search_fields = ('line_text',)

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(News , NewsAdmin)
admin.site.register(Video , VideoAdmin)
admin.site.register(LyricLine , LyricLineAdmin)