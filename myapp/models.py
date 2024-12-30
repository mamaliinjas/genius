from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image , ImageOps
from django.utils.timezone import now
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings


# Create your models here.
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=settings.SPOTIPY_CLIENT_ID,
    client_secret=settings.SPOTIPY_CLIENT_SECRET
))

GENRE_CHOICES=[
    ('rap' , 'Rap'),
    ('pop' , 'Pop'),
    ('rnb' , 'R&B'),
    ('country' , 'Country'),
    ('rock' , 'Rock'),    
]

class Video(models.Model):
    title=models.CharField(max_length=50)
    description=models.TextField(blank=True , null=True)
    embed_code=models.TextField(null=True , blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    artist = models.ForeignKey('Artist' , on_delete=models.CASCADE , null=True , blank=True)
    
    def __str__(self):
        return self.title





def crop_and_resize(image_path, output_size=(1080, 720), crop_coords=None):
    with Image.open(image_path) as img:
        if crop_coords:
            img = img.crop(crop_coords)  # crop_coords: (left, upper, right, lower)

        original_width, original_height = img.size
        target_width, target_height = output_size

        aspect_ratio = original_width / original_height

        if original_width > original_height:
            new_width = target_width
            new_height = int(target_width / aspect_ratio)
        else:
            new_height = target_height
            new_width = int(target_height * aspect_ratio)

        if new_width > target_width:
            new_width = target_width
            new_height = int(target_width / aspect_ratio)

        if new_height > target_height:
            new_height = target_height
            new_width = int(target_height * aspect_ratio)

        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        img.save(image_path)

class Artist(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='artist_profiles/')
    cover_picture = models.ImageField(upload_to='artist_covers/', null=True, blank=True)
    aka = models.CharField(max_length=200, null=True, blank=True)
    spotify_id=models.CharField(max_length=250 , null=True ,  blank=True)
    monthly_listeners = models.IntegerField(default=0)
    views = models.PositiveBigIntegerField(default=0)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, null=True, blank=True)
    crop_coords = models.CharField(
        max_length=50, 
        null=True, 
        blank=True,
        help_text="Enter crop coordinates as 'left,upper,right,lower' (e.g., 100,50,800,600). Leave blank for default cropping."
    )
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    soundcloud = models.URLField(null=True, blank=True)
    spotify = models.URLField(null=True, blank=True)
    youtube=models.URLField(null=True , blank=True)
    telegram=models.URLField(null=True , blank=True)
    
    def get_monthly_listeners(self):
        """Method to get artist's monthly listeners from Spotify"""
        try:
            artist_data = sp.artist(self.spotify_id)
            return artist_data['followers']['total']  # Return the total monthly listeners
        except Exception as e:
            print(f"Error fetching artist data: {e}")
            return None    
    
    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        if self.cover_picture:
            cover_path = self.cover_picture.path

            crop_coords = None
            if self.crop_coords:
                crop_coords = tuple(map(int, self.crop_coords.split(',')))

            crop_and_resize(cover_path, crop_coords=crop_coords)
    
    def __str__(self):
        return self.name
    

    
class Album(models.Model):
    title=models.CharField(max_length=200)
    release_date=models.DateField(blank=True, null=True) 
    cover_photo=models.ImageField(upload_to='album_covers/' , blank=True , null=True)
    profile_photo=models.ImageField(upload_to='album_profiles/' , blank=True , null=True)
    artist = models.ForeignKey('Artist' , on_delete=models.CASCADE , related_name='albums')
    views=models.PositiveIntegerField(default=0)
    genre=models.CharField(max_length=20 , choices=GENRE_CHOICES , null=True , blank=True)
      
    def __str__(self):
          return self.title
      
    
class Song(models.Model):
    artist=models.ForeignKey('Artist' , on_delete=models.CASCADE , related_name='songs')
    title=models.CharField(max_length=200)
    duration=models.DurationField()
    lyrics = models.TextField(blank=True, null=True)
    album = models.ForeignKey('Album', on_delete=models.CASCADE, related_name='songs', blank=True, null=True)
    views=models.PositiveIntegerField(default=0)
    release_date=models.DateField(blank=True, null=True)
    genre=models.CharField(max_length=20 , choices=GENRE_CHOICES , null=True, blank=True)
    song_cover= models.ImageField(upload_to='song_covers/', null=True, blank=True)    
    def __str__(self):
        return self.title
    
    
class News(models.Model):
    title=models.CharField(max_length=250)
    content=models.TextField()
    cover_image=models.ImageField(upload_to='news_covers/' , null=True , blank=True)
    published_date=models.DateTimeField(default= now)
    is_featured=models.BooleanField(default=False)
    detailed_description=models.TextField(null=True , blank=True)
    def save(self, *args , **kwargs):
        if self.is_featured:
            News.objects.filter(is_featured=True).exclude(pk=self.pk).update(is_featured=False)
        super().save(*args , **kwargs)
        if self.cover_image:
            img=Image.open(self.cover_image.path)
            
            desired_size=(1200 , 800)
            
            img=ImageOps.fit(img ,desired_size , Image.Resampling.LANCZOS)   
            img.save(self.cover_image.path)
            
    def __st__(self):
        return self.title
    
class LyricLine(models.Model):
    song=models.ForeignKey(Song , on_delete=models.CASCADE ,related_name='lyric_lines')
    line_text=models.TextField()
    timestamp=models.TimeField(help_text="Time when the line starts in the song (HH:MM:SS)")
    meaning=models.TextField(null=True , blank=True , help_text="Optional: Explanation or meaning of the lyric")
    def __str__(self):
        return f"{self.song.title} - {self.line_text[:30]}"