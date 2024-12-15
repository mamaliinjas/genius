from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.models import  User
from django.contrib import messages
from django.contrib.auth import login as auth_login , authenticate
from .models import Artist , Song , Album , News , Video , LyricLine
from django.db.models import Q , Sum
from django.http import JsonResponse
from datetime import timedelta , date
import json
from colorthief import ColorThief
from django.conf import settings
import os
from django.contrib.auth import logout
import requests

# Create your views here.
SPOTIFY_CLIENT_ID='82b8a20a9bfb48b0a2eaf86682819151'
SPOTIFY_CLIENT_SECRET='7d4a43b5a12b4dfb99067e1e88a6e824'
SPOTIFY_REDIRECT_URI='http://localhost:8000/callback/'

def spotify_login(request):
    auth_url=(
        f"https://accounts.spotify.com/authorize"
        f"?response_type=code"
        f"&client_id={SPOTIFY_CLIENT_ID}"
        f"&redirect_uri={SPOTIFY_REDIRECT_URI}"
        f"&scope=user-library-read user-read-private"
    )
    return redirect (auth_url)


def spotify_callback(request):
    code=request.GET.get('code')
    token_url = "https://accounts.spotify.com/api/token" 
    response=requests.post(
        token_url ,
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET,
        },
    )
    
    tokens=response.json()
    access_token= tokens['access_token']
    refresh_token=tokens['refresh_token'] 
    
    request.session['spotify_access_token'] = access_token
    request.session['spotify_refresh_token'] = refresh_token
    
    return redirect('home')


def get_user_playlists(request):
    access_token = request.session.get('spotify_access_token')
    if not access_token:
        return redirect('spotify_login')  # If not logged in, redirect to login
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    playlists_url = 'https://api.spotify.com/v1/me/playlists'
    response = requests.get(playlists_url, headers=headers)
    playlists = response.json()
    
    return render(request, 'playlists.html', {'playlists': playlists})



def home(request):
    top_news = News.objects.filter(is_featured=True).order_by('-published_date')[:1]
    latest_news = News.objects.filter(is_featured=False).order_by('-published_date')[:4]
    latest_videos=Video.objects.all().order_by('-created_at')[:3]
    return render(request , 'home.html'  , {
        'top_news' : top_news , 
        'latest_news' : latest_news,
        'videos' : latest_videos
    })

def ajax_search(request):
    query = request.GET.get('q', '').strip()
    data = {
        'artists': [],
        'songs': [],
        'albums': [],
        'lyrics_results': [],
    }

    try:
        if query:
            # Search for artists
            data['artists'] = list(Artist.objects.filter(name__icontains=query).values('id', 'name', 'profile_picture'))

            # Search for songs
            data['songs'] = list(Song.objects.filter(title__icontains=query).values('id', 'title', 'artist__name'))

            # Search for albums
            data['albums'] = list(Album.objects.filter(title__icontains=query).values('id', 'title', 'artist__name'))

            # Search for lyrics if no other results
            if not (data['artists'] or data['songs'] or data['albums']):
                data['lyrics_results'] = list(Song.objects.filter(lyrics__icontains=query).values('id', 'title', 'artist__name', 'lyrics'))

    except Exception as e:
        # Catch any unexpected error and log it
        print(f"Error in ajax_search view: {e}")
        data['error'] = str(e)

    return JsonResponse(data)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        # Save user using Django's User model
        from django.contrib.auth.models import User
        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, 'An error occurred: ' + str(e))
            return redirect('register')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        login_input = request.POST['login_input']
        password = request.POST['password']
        
 
        try:
            user = User.objects.get(email=login_input)
            username = user.username
        except User.DoesNotExist:
            username = login_input

     
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'Account does not exist. Please register.')
            else:
                messages.error(request, 'Incorrect password.')
    return render(request, 'login.html') 
   
def logout_view(request):
    previous_url=request.META.get('HTTP_REFERER' , 'home')
    logout(request)
    return redirect(previous_url)

def video_section(request):
    videos = Video.objects.all().order_by('-created_at')
    return render(request , 'video_section.html' , {
        'videos' : videos
    })
    
    
def artist_profile(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    songs =Song.objects.filter(artist=artist).order_by('-views')[:10]
    if request.method == 'POST' and 'song_id' in request.POST:
        song = get_object_or_404(Song , pk=request.POST['song_id'])
        song.views += 1
        song.save()
    albums = artist.albums.all().order_by('-release_date') 
    
    videos=Video.objects.filter(artist=artist).order_by('-created_at') 
    return render(request, 'artist_profile.html', {
        'artist': artist,
        'albums': albums,
        'songs': songs,
        'videos':videos ,
        })


def album_details(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    songs_in_album = album.songs.all()
    return render(request, 'album_details.html', {'album': album, 'songs_in_album': songs_in_album})




def song_details(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    lyrics = song.lyric_lines.order_by('timestamp')
    dominant_color = (0, 0, 0)  # Default black color

    # Check if song has a valid cover
    song_cover_path = song.song_cover.path if song.song_cover else None
    if song_cover_path and os.path.isfile(song_cover_path):
        try:
            color_thief = ColorThief(song_cover_path)
            dominant_color = color_thief.get_color(quality=1)
        except Exception as e:
            print(f"Error with ColorThief: {e}")
    else:
        print("Song cover not found or invalid.")

    return render(request, 'song_details.html', {
        'song': song,
        'dominant_color': f'rgb{dominant_color}',
        'lyrics' : lyrics,
    })

def news_section(request):
    top_news=News.objects.filter(is_featured=True).order_by('-published_date')[:1]
    latest_news=News.objects.filter(is_featured=False).order_by('-published_date')[:4]
    
    return render (request , 'news_section.html' , {
        'top_news': top_news,
        'latest_news':latest_news,
    })

def news_detail(request , news_id ):
    try:
        news =News.objects.get(id=news_id)
    except News.DoesNotExist:
        return render(request , '404.html' , status=404)
    return render(request , 'news_detail.html' , { 'news' : news })

def chart_section(request):
    # Get filters from query parameters
    type_filter = request.GET.get('type', 'song')
    genre_filter = request.GET.get('genre', 'all')
    time_filter = request.GET.get('time', 'all')

    # Data structure to store results
    data = {'results': [], 'chart_data': {'labels': [], 'values': [], 'images': []}}

    today = date.today()

    # Handle time filtering (day, week, month)
    if time_filter == 'day':
        start_date = today - timedelta(days=1)
    elif time_filter == 'week':
        start_date = today - timedelta(days=7)
    elif time_filter == 'month':
        start_date = today - timedelta(days=30)
    else:
        start_date = None

    # Handle type filtering (song, album, artist, lyric)
    if type_filter == 'song':
        queryset = Song.objects.all()
    elif type_filter == 'album':
        queryset = Album.objects.all()
    elif type_filter == 'artist':
        queryset = Artist.objects.all()
    elif type_filter == 'lyric':
        queryset = Song.objects.filter(lyrics__isnull=False)
    else:
        return JsonResponse({'error': 'invalid type filter'}, status=400)

    # Handle genre filtering
    if genre_filter != 'all' and type_filter in ['song', 'album' , 'artist' , 'lyric']:
        queryset = queryset.filter(genre=genre_filter)

    # Handle date filtering
    if start_date and type_filter in ['song', 'album']:
        queryset = queryset.filter(release_date__gte=start_date)

    # Order by views and limit to top 10
    queryset = queryset.order_by('-views')[:10]

    # Build the results and chart data
    for item in queryset:
        if type_filter == 'song':
            data['results'].append({
                'id': item.id,
                'title': item.title,
                'artist': item.artist.name,
                'views': item.views,
                'image': item.song_cover.url if item.song_cover else None
            })
            data['chart_data']['labels'].append(item.title)
            data['chart_data']['values'].append(item.views)
            data['chart_data']['images'].append(item.song_cover.url if item.song_cover else None)

        elif type_filter == 'album':
            data['results'].append({
                'id': item.id,
                'title': item.title,
                'artist': item.artist.name,
                'views': item.views,
                'image': item.cover_photo.url if item.cover_photo else None
            })
            data['chart_data']['labels'].append(item.title)
            data['chart_data']['values'].append(item.views)
            data['chart_data']['images'].append(item.cover_photo.url if item.cover_photo else None)

        elif type_filter == 'artist':
            data['results'].append({
                'id': item.id,
                'name': item.name,
                'views': item.views,
                'image': item.profile_picture.url if item.profile_picture else None
            })
            data['chart_data']['labels'].append(item.name)
            data['chart_data']['values'].append(item.views)
            data['chart_data']['images'].append(item.profile_picture.url if item.profile_picture else None)

    return JsonResponse(data)


