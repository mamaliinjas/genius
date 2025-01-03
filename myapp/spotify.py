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
    # Loop through artists and update their monthly listeners from Spotify
    for artist in Artist.objects.exclude(spotify_id__isnull=True):
        # Get the monthly listeners using the Spotify ID
        monthly_listeners = get_artist_listeners(artist.spotify_id)
        
        # Only update if we successfully fetched the listeners
        if monthly_listeners is not None:
            artist.monthly_listeners = monthly_listeners
            artist.save()
