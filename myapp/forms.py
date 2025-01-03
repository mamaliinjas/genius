from django import forms
from .models import Artist

class ArtistAdminForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'spotify_id', 'monthly_listeners']

    def clean_spotify_id(self):
        spotify_url = self.cleaned_data.get('spotify_id')
        if spotify_url:
            # Extract Spotify ID from the URL
            import re
            match = re.search(r"spotify\.com/artist/([a-zA-Z0-9]+)", spotify_url)
            if match:
                return match.group(1)  # Return only the Spotify ID
            else:
                raise forms.ValidationError("Invalid Spotify URL.")
        return spotify_url