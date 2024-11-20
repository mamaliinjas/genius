from django.urls import path 
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns=[
    path('' , views.home , name='home'),
    path('register' , views.register , name='register'),
    path('login' , views.login , name='login'),
    path('artist/<int:artist_id>/' , views.artist_profile , name='artist_profile'),
    path('album/<int:album_id>/' , views.album_details , name='album_details'),
    path('song/<int:song_id>/' , views.song_details , name='song_details'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)