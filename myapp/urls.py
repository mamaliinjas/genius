from django.urls import path 
from . import views



urlpatterns=[
    path('' , views.home , name='home'),
    path('register' , views.register , name='register'),
    path('login' , views.login , name='login'),
    path('artist/<int:artist_id>/' , views.artist_profile , name='artist_profile'),
    path('album/<int:album_id>/' , views.album_details , name='album_details'),
    path('song/<int:song_id>/' , views.song_details , name='song_details'),
    path('track/<int:track_id>/' ,views.track_details , name='track_details'),
    
]