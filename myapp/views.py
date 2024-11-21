from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.models import  User
from django.contrib import messages
from django.contrib.auth import login as auth_login , authenticate
from .models import Artist , Song , Album
from django.db.models import Q
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request , 'home.html')

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
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password != password2:
            messages.info(request, 'Passwords do not match')
            return render(request, 'register.html', {'username': username, 'email': email})
        
        if User.objects.filter(email=email).exists():
            messages.info(request, 'EMAIL IS ALREADY USED')
            return render(request, 'register.html', {'username': username, 'email': email})
        
        if User.objects.filter(username=username).exists():
            messages.info(request, 'USERNAME IS TAKEN')
            return render(request, 'register.html', {'username': username, 'email': email})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return redirect('login')

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
            messages.info(request, 'Invalid email/username or password')
            return redirect('login') 
    return render(request, 'login.html') 
   

def artist_profile(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    albums = artist.albums.all()
    songs = artist.songs.all()    
    return render(request, 'artist_profile.html', {'artist': artist, 'albums': albums, 'songs': songs})


def album_details(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    songs_in_album = album.songs.all()  
    return render(request, 'album_details.html', {'album': album, 'songs_in_album': songs_in_album})


def song_details(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    return render(request, 'song_details.html', {'song': song})


            