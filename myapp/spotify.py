from myapp.models import Artist, Song
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=settings.SPOTIPY_CLIENT_ID,
    client_secret=settings.SPOTIPY_CLIENT_SECRET
))

def get_artist_listeners(spotify_id):
    try:
        artist = sp.artist(spotify_id)
        print(artist)  # Debugging line to see if you are getting the correct response
        return artist['followers']['total']  # Monthly listeners
    except Exception as e:
        print(f"Error fetching artist data: {e}")
        return None


def update_spotify_views():
    # Update artists' monthly listeners
    for artist in Artist.objects.exclude(spotify_id__isnull=True):
        artist.monthly_listeners = get_artist_listeners(artist.spotify_id)
        artist.save()
