from django.urls import path , include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter 
from .views import ArtistViewSet, AlbumViewSet, SongViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = DefaultRouter()
router.register(r'artists', ArtistViewSet, basename='artist')
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'songs', SongViewSet, basename='song')

urlpatterns=[
    path('' , views.home , name='home'),
    path('register' , views.register , name='register'),
    path('login' , views.login , name='login'),
    path('logout/' , views.logout_view , name='logout') , 
    path('artist/<int:artist_id>/' , views.artist_profile , name='artist_profile'),
    path('album/<int:album_id>/' , views.album_details , name='album_details'),
    path('song/<int:song_id>/' , views.song_details , name='song_details'),
    path('ajax_search/' , views.ajax_search , name='ajax_search'),
    path('news/' , views.news_section , name='news_section'),
    path('chart_data/', views.chart_section, name='chart_section'),
    path('news/<int:news_id>' , views.news_detail , name='news_detail'),
    path('video_section/' , views.video_section , name='video_section'),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # ReDoc UI
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)