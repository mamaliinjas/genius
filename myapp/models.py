from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
from django.utils.timezone import now

# Create your models here.
GENRE_CHOICES=[
    ('rap' , 'Rap'),
    ('pop' , 'Pop'),
    ('rnb' , 'R&B'),
    ('country' , 'Country'),
    ('rock' , 'Rock'),    
]


def validate_cover_image(image):
   img=Image.open(image)
   width , height = img.size
   if width != 1920:
        raise ValidationError("Cover image width must be 1920px.")

   if not (400 <= height <= 1080):
        raise ValidationError(
            "Cover image height must be between 400px and 1080px."
        )
class Artist(models.Model):
    name=models.CharField(max_length=100)
    bio=models.TextField()
    profile_picture=models.ImageField(upload_to='artist_profiles/')
    cover_picture=models.ImageField(upload_to='artist_covers/' , validators=[validate_cover_image] , null=True , blank=True)
    aka=models.CharField(max_length=200 , null=True , blank=True)
    views=models.PositiveBigIntegerField(default=0)
    genre=models.CharField(max_length=20 , choices=GENRE_CHOICES , null=True , blank=True)
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
    audio_file=models.FileField(upload_to='songs/' , blank=True , null=True)
    lyrics = models.TextField(blank=True, null=True)
    album = models.ForeignKey('Album', on_delete=models.CASCADE, related_name='songs', blank=True, null=True)
    views=models.PositiveIntegerField(default=0)
    release_date=models.DateField(blank=True, null=True)
    genre=models.CharField(max_length=20 , choices=GENRE_CHOICES , null=True, blank=True)
    cover_photo = models.ImageField(upload_to='song_covers/', null=True, blank=True) 
    
    def __str__(self):
        return self.title
    
    
class News(models.Model):
    title=models.CharField(max_length=250)
    content=models.TextField()
    cover_image=models.ImageField(upload_to='news_covers/' , null=True , blank=True)
    published_date=models.DateTimeField(default= now)
    is_featured=models.BooleanField(default=False)
    def save(self, *args , **kwargs):
        if self.is_featured:
            News.objects.filter(is_featured=True).exclude(pk=self.pk).update(is_featured=False)
        super().save(*args , **kwargs)
            
    def __st__(self):
        return self.title
    
    