from django.db import models

# Create your models here.
class Artist(models.Model):
    name=models.CharField(max_length=100)
    bio=models.TextField()
    profile_picture=models.ImageField(upload_to='artist_profiles/')
    cover_picture=models.ImageField(upload_to='artist_covers/')
    
    def __str__(self):
        return self.name
    
class Album(models.Model):
    title=models.CharField(max_length=200)
    release_date=models.DateField(blank=True, null=True) 
    cover_photo=models.ImageField(upload_to='album_covers/' , blank=True , null=True)
    profile_photo=models.ImageField(upload_to='album_profiles/' , blank=True , null=True)
    artist = models.ForeignKey('Artist' , on_delete=models.CASCADE , related_name='albums')
      
    def __str__(self):
          return self.title
      
    
class Song(models.Model):
    artist=models.ForeignKey('Artist' , on_delete=models.CASCADE , related_name='songs')
    title=models.CharField(max_length=200)
    duration=models.DurationField()
    audio_file=models.FileField(upload_to='songs/' , blank=True , null=True)
    lyrics = models.TextField(blank=True, null=True)
    album = models.ForeignKey('Album', on_delete=models.CASCADE, related_name='songs', blank=True, null=True)
    
    def __str__(self):
        return self.title