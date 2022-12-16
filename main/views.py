from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Album, Artist, Track, Genre, AlbumRating, TrackRating
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, NewAlbumForm, RateAlbumForm
from django.db.models import Avg
from main.scripts.scrape import Scrape

from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView

# Create your views here.
def single_slug(request, single_slug):

	# Handling for Genre page
	# If slug is a genre slug, redirect to genre.html with a dictionary matching albums to their slugs
	genres = [g.genre_slug for g in Genre.objects.all()] #All genre slugs
	if single_slug in genres:
		matching_albums = Album.objects.filter(genre__genre_slug=single_slug) #Get Album with corresponding genre

		album_urls = {}
		for m in matching_albums.all():
			# part_one = Track.objects.filter(album_name__album_name=m.album_name).earliest("track_number")
			# album_urls[m] = part_one.track_slug
			album_urls[m] = m.album_slug

		return render(request,
			"main/genre.html",
			{"albums":album_urls})


	# Handling for album page
	# If slug is an album slug, redirect to album.html with the album object, artist object, and all album ratings for that album.
	albums = [a.album_slug for a in Album.objects.all()]
	if single_slug in albums:
		this_album = Album.objects.get(album_slug=single_slug)
		this_artist = Artist.objects.get(artist_name=this_album.artist_name)
		album_ratings = AlbumRating.objects.filter(album_name__album_name=this_album.album_name)
		average_rating = album_ratings.aggregate(Avg('rating'))
		album_tracks = Track.objects.filter(album_name__album_name=this_album.album_name)

		return render(request,
			"main/album.html",
			{"album":this_album, "artist":this_artist, "ratings":album_ratings, "score":average_rating['rating__avg'], "tracks":album_tracks})

	# Handling for track page
	# If slug is an track slug, redirect to track.html 
	tracks = [t.track_slug for t in Track.objects.all()]
	if single_slug in tracks:
		this_track = Track.objects.get(track_slug=single_slug)
		this_album = Album.objects.get(album_name=this_track.album_name)
		this_artist = Artist.objects.get(artist_name=this_track.artist_name)
		track_ratings = TrackRating.objects.filter(track_name__track_name=this_track.track_name)
		average_rating = track_ratings.aggregate(Avg('rating'))

		album_tracks = Track.objects.filter(album_name__album_name=this_album.album_name)

		return render(request,
			"main/track.html",
			{"track": this_track, "album":this_album, "artist":this_artist, "ratings":track_ratings, "score":average_rating['rating__avg'], "tracks":album_tracks})

	return HttpResponse("{} does not correspond to anything.".format(single_slug))

# Homepage, shows all genres : Later shows different pages to redirect to
def homepage(request):
	return render(request=request,
		template_name="main/genres.html",
		context={"genres": Genre.objects.all})

# Register view, initially renders register.html, where the user can fill out a form that redirects back here with the request.method = POST
# Once user is created, logs user in and redirects to homepage
def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get("username")
			messages.success(request, "New Account Created: {}".format(username))
			login(request, user)
			return redirect("main:homepage")
		else:
			for msg in form.error_messages:
				messages.error(request, "{}: {}".format(msg, form.error_messages[msg]))

	form = NewUserForm
	return render(request,
		"main/register.html",
		context={"form": form})

# Logout and redirect to homepage
def logout_request(request):
	logout(request)
	messages.info(request, "Logged out.")
	return redirect("main:homepage")

# Login view initially renders login.html where user fills out login form and redirects here with method == POST
# Authenticate user and then log them in and redirect to homepage
def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)

			if user is not None:
				login(request, user)
				messages.success(request, "Logged in as: {}".format(username))
				return redirect("main:homepage")
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Invalid input.")

	form = AuthenticationForm()
	return render(request,
		"main/login.html",
		{"form":form})

# Add album initially renders addalbum.html where user can fill out NewAlbumForm.
# Redirects back to genre where Album was added
# Currently runs into error when adding album with an unregistered artist, although it creates the artist - Go back and retry and it should work - NEEDS FIX
def add_album(request):
	if request.method == "POST":
		form = NewAlbumForm(request.POST)
		if form.is_valid():
			album = form.save()
			album_name = form.cleaned_data.get('album_name')
			genre = form.cleaned_data.get('temp_genre')

			genre_slug = Genre.objects.get(genre=genre).genre_slug
			print(genre_slug)

			messages.success(request, "New Album Posted")

			return redirect('main:single_slug', genre_slug)
		else:
			messages.error(request, "Invalid input.")

	form = NewAlbumForm
	return render(request,
		"main/addalbum.html",
		context={"form": form})
			# album_name = form.cleaned_data.get('album_name')
			# artist_name = form.cleaned_data.get('artist_name')
			# release_date = form.cleaned_data.get('release_date')
			# album_description = form.cleaned_data.get('album_description')
			# is_single = form.cleaned_data.get('is_single')
			# genre = form.cleaned_data.get('genre')
			# album_slug = form.cleaned_data.get('album_slug')

# Once album is created, it is an empty page with nothing but the information provided in the form
# Takes in slug of the album it wants to update
# Scrapes tracklist based off artist name and album name
# For each track in the tracklist, scrapes lyrics
# Gets album cover using 3rd track in the list and artist name - NEEDS TO BE UPDATED TO USE ALBUM NAME
# Very buggy and unreliable
def update_album(request, single_slug):
	albums = [a.album_slug for a in Album.objects.all()]
	if single_slug in albums:
		this_album = Album.objects.get(album_slug=single_slug) 
		this_artist = Artist.objects.get(artist_name=this_album.artist_name) 

		album_name = this_album.album_name
		artist_name = this_artist.artist_name

		# Scraping the lyrics does not always work, I still don't understand why, sometimes the page takes too long to load so the request doesn't pull the data
		# This constant is the number of times it should try to scrape lyrics for each track
		LOOP_COUNT = 5
		count = 0

		# Get Track List
		track_list = Scrape.getTrackList(this_artist.artist_name, this_album.album_name)

		# Enumerate to get Track Numbers in order
		for i, ele in enumerate(track_list, start=1):
			# Create Slug
			track_slug = Scrape.createSlug(artist_name, ele)

			# Temporary fix, uses the third song to find the cover for the album, makes sure that a file is not already stored
			if i == 2 and this_album.album_cover_url[-3:] not in ['png', 'jpg', 'bmp']:
				this_album.album_cover_url = Scrape.getAlbumCoverURL(artist_name, ele)

			# CHECK if artist already has track with the same name
			artist_tracks = Track.objects.filter(artist_name__artist_name=artist_name)
			track_names = [t.track_name for t in artist_tracks]
			this_track = ""

			# If this track exists in the list of this artist's tracks, get the track and update it's fields
			if ele in track_names:
				this_track = Track.objects.get(track_name=ele, artist_name=this_artist)
				this_track.album_name = this_album
				this_track.track_number = i
				if this_track.track_lyrics == "404" or this_track.track_lyrics == "":
					track_lyrics = Scrape.getSongLyrics(artist_name, ele)

					# Loop until lyrics are retrieved or counter runs out
					while(track_lyrics == "404" and count < LOOP_COUNT):
						track_lyrics = Scrape.getSongLyrics(artist_name, ele)
						count+=1

				this_track.track_slug = track_slug
				this_track.save() # Save changes to model
			else:	# If it doesn't exist
				track_lyrics = Scrape.getSongLyrics(artist_name, ele)
				while(track_lyrics == "404" and count < LOOP_COUNT):
					track_lyrics = Scrape.getSongLyrics(artist_name, ele)
					count+=1
				this_track = Track(track_name=ele, album_name=this_album, artist_name=this_artist, track_number=i, track_lyrics=track_lyrics, track_slug=track_slug)
				this_track.save()
			count = 0

		# print(track_list)
		this_album.save() # Save changes to model
		this_artist.artist_slug = Scrape.createSlug(artist_name, "")

		this_artist.save()
		return redirect('main:single_slug', single_slug)

# Account view renders user information and previous ratings
def account(request):
	user = request.user

	album_ratings = AlbumRating.objects.filter(username__username=user.username)
	track_ratings = TrackRating.objects.filter(username__username=user.username)
	albums = Album.objects.all()
	tracks = Track.objects.all()

	return render(request=request,
		template_name="main/account.html",
		context={"albums_ratings" : album_ratings, "track_ratings" : track_ratings, "albums" : albums, "tracks" : tracks})

def rate_album(request):
	form = RateAlbumForm(request.POST)
	return render(request,
		"main/ratealbum.html",
		context={"form": form})

class RateAlbumView(BSModalCreateView):
    template_name = 'main/ratealbum.html'
    form_class = RateAlbumForm
    success_message = 'Success: AlbumRated.'
    success_url = reverse_lazy('')