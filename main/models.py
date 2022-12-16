from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

# Create your models here.

class Genre(models.Model):
	genre = models.CharField(max_length=200)
	genre_description = models.TextField(default="No Description")
	genre_image_url = models.CharField(max_length=200, default="https://img.discogs.com/G0haDbUa-_stv3xTv9R5ip4fAKo=/fit-in/600x600/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/R-238369-1490362449-5582.jpeg.jpg")

	genre_slug = models.CharField(max_length=200, default=1)

	class Meta:
		verbose_name_plural = "Genres"

	def __str__(self):
		return self.genre

class Artist(models.Model):
	artist_name = models.CharField(max_length=200)
	artist_age = models.IntegerField()
	label_name = models.CharField(max_length=200)
	artist_description = models.TextField(default="No Description")
	artist_image_url = models.CharField(max_length=200, default="https://images.genius.com/6d0fbbc7ce189a8c81671ef92546446e.1000x1000x1.png")

	artist_slug = models.CharField(max_length=200, default=1)

	class Meta:
		verbose_name_plural = "Artists"

	def __str__(self):
		return self.artist_name


class Album(models.Model):
	album_name = models.CharField(max_length=200)
	artist_name = models.ForeignKey(Artist, default=1, verbose_name="Artist", on_delete=models.SET_DEFAULT)
	album_cover_url = models.CharField(max_length=200, default="https://assets.genius.com/images/default_cover_image.png?1596138983")

	# artist_name = models.CharField(max_length=200)
	release_date = models.DateField("release date")
	album_description = models.TextField()
	is_single = models.BooleanField(default=False)
	genre = models.ForeignKey(Genre, default=1, verbose_name="Genre", on_delete=models.SET_DEFAULT)

	album_slug = models.CharField(max_length=200, default=1)

	author = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)

	class Meta:
		verbose_name_plural = "Albums"
		unique_together = ["artist_name", "album_name"]

	def __str__(self):
		return self.album_name

class Track(models.Model):
	track_name = models.CharField(max_length=200)
	album_name = models.ForeignKey(Album, default=1, verbose_name="Album", on_delete=models.SET_DEFAULT)
	artist_name = models.ForeignKey(Artist, default=1, verbose_name="Artist", on_delete=models.SET_DEFAULT)
	track_number = models.IntegerField(default=1)
	track_lyrics = models.TextField(default="")
	
	track_slug = models.CharField(max_length=200, default=1)

	class Meta:
		verbose_name_plural = "Tracks"
		unique_together = ["artist_name", "track_name"]

	def __str__(self):
		return "{} by {}".format(self.track_name, self.artist_name)

class AlbumRating(models.Model):
	username = models.ForeignKey(User, default=1, verbose_name="User", on_delete=models.CASCADE)
	album_name = models.ForeignKey(Album, default=1, verbose_name="Album", on_delete=models.CASCADE)
	rating = models.IntegerField(validators=[MaxValueValidator(10)])
	review = models.TextField(default="")

	class Meta:
		verbose_name_plural = "Album Ratings"

	def __str__(self):
		return "{} - {} - {}".format(self.album_name, self.username, self.rating)

class TrackRating(models.Model):
	username = models.ForeignKey(User, default=1, verbose_name="User", on_delete=models.CASCADE)
	track_name = models.ForeignKey(Track, default=1, verbose_name="Track", on_delete=models.CASCADE)
	rating = models.IntegerField(validators=[MaxValueValidator(10)])
	review = models.TextField(default="")

	class Meta:
		verbose_name_plural = "Track Ratings"

	def __str__(self):
		return "{} - {} - {}".format(self.album_name, self.username, self.rating)
