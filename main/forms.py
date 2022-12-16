from django import forms
from .models import Album, Genre, Artist, AlbumRating, TrackRating
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bootstrap_modal_forms.forms import BSModalModelForm

class RateAlbumForm(BSModalModelForm):
	class Meta:
		model = AlbumRating
		fields = ['album_name', 'rating', 'review']

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class NewAlbumForm(forms.ModelForm):
	album_name = forms.CharField(label='Album Name', max_length=200)
	temp_artist = forms.CharField(label='Artist Name', max_length=200)
	release_date = forms.DateField(label="Release Date", initial='YYYY-MM-DD')

	# album_description = forms.TextField()
	# is_single = forms.BooleanField()

	temp_genre = forms.CharField(label='Genre', max_length=200)

	album_slug = forms.CharField(label='Album Slug', initial='album-name-artistname', max_length=200)

	class Meta:
		model = Album
		fields = ['album_name', 'temp_artist', 'release_date', 'temp_genre', 'album_slug']

	def save(self, commit=True):
		album = super(NewAlbumForm, self).save(commit=False)
		album.album_name = self.cleaned_data['album_name']

		artists = [a.artist_name for a in Artist.objects.all()]
		artist_name = self.cleaned_data['temp_artist']
		if artist_name in artists:
			album.artist_name = Artist.objects.get(artist_name=artist_name)
		else:
			album.artist_name = Artist(artist_name=self.cleaned_data['temp_artist'], artist_age=0, label_name="", artist_slug="-1")
			album.artist_name.save()

		genres = [g.genre for g in Genre.objects.all()]
		genre = self.cleaned_data['temp_genre']
		if genre in genres:
			album.genre = Genre.objects.get(genre=genre)
		else:
			album.genre = Genre.objects.get(genre="Other")

		album.release_date = self.cleaned_data['release_date']
		# album.album_description = self.cleaned_data['album_description']
		# album.is_single = self.cleaned_data['is_single']
		album.album_slug = self.cleaned_data['album_slug']

		if commit:
			album.save()
		return album