from django.contrib import admin
from .models import Artist, Album, Song , News , Video ,LyricLine, LyricMeaning
from .forms import ArtistAdminForm
from .spotify import get_artist_listeners
# Register your models here.



class ArtistAdmin(admin.ModelAdmin):
    search_fields = ['name', 'bio', 'aka', 'twitter', 'spotify_id', 'soundcloud', 'spotify', 'instagram', 'telegram', 'youtube']
    list_display = ['name', 'bio', 'profile_picture', 'aka', 'spotify_id', 'get_monthly_listeners', 'twitter', 'instagram', 'soundcloud', 'spotify', 'telegram', 'youtube']
    list_filter = ['name']
    form = ArtistAdminForm

    # Explicitly define the fields to be displayed in the form
    fields = [
        'name',
        'bio',
        'profile_picture',
        'cover_picture',
        'crop_coords',
        'aka',
        'spotify_id',
        'monthly_listeners',
        'views',
        'genre',
        'twitter',
        'instagram',
        'soundcloud',
        'spotify',
        'youtube',
        'telegram',
    ]

    def save_model(self, request, obj, form, change):
        """
        Override the save_model method to update monthly listeners.
        """
        # Save the Artist object
        super().save_model(request, obj, form, change)

        # Fetch and update monthly listeners if Spotify ID is provided
        if obj.spotify_id:
            listeners = get_artist_listeners(obj.spotify_id)
            if listeners is not None:
                obj.monthly_listeners = listeners
                obj.save()
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
    list_display = ('line_text', 'song', 'is_highlighted')
    list_filter = ('song', 'is_highlighted')
    search_fields = ('line_text', 'song__title')

class LyricMeaningAdmin(admin.ModelAdmin):
    list_display = ('get_lyric_lines', 'created_at')
    search_fields = ('meaning_text',)

    def get_lyric_lines(self, obj):
        return ", ".join([line.line_text[:20] for line in obj.lyric_lines.all()])
    get_lyric_lines.short_description = "Lyric Lines"

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(News , NewsAdmin)
admin.site.register(Video , VideoAdmin)
admin.site.register(LyricLine , LyricLineAdmin)
admin.site.register(LyricMeaning , LyricMeaningAdmin)