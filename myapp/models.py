from django.db import models

# Create your models here.
class artist(models.model):
    name=models.CharField(max_length=100)
    bio=models.TextField()
    profile_picture=models.ImageField(upload_to='artist_profiles/')
    cover_picture=models.ImageField(upload_to='artist_covers/')
    
    def __str__(self):
        return self.name
    
class album(models.model):
    title=models.CharField(max_length=200)
    release_date=models.DateField(blank=True, null=True) 
    cover_photo=models.ImageField(upload_to='album_covers/' , blank=True , null=True)
    profile_photo=models.ImageField(upload_to='album_profiles/' , blank=True , null=True)
    artist = models.ForeignKey('artist' , on_delete=models.CASCADE , related_name='albums')
      
    def __str__(self):
          return self.title
      
class track(models.model):
    album=models.ForeignKey(album , on_delete=models.CASCADE , related_name='tracks')
    name=models.CharField(max_length=250)
    duration=models.DurationField()
    
    def __str__(self):
        return f"{self.name} - {self.album.name}"      
class song(models.model):
    artist=models.ForeignKey('artist' , on_delete=models.CASCADE , related_name='songs')
    title=models.CharField(max_length=200)
    duration=models.DurationField()
    audio_file=models.FileField(upload_to='songs/' , blank=True , null=True)
    
    def __str__(self):
        return self.title