from django.contrib import admin
from .models import Album, Artist, Genre, Track, TrackRating, AlbumRating
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.

# class AlbumAdmin(admin.ModelAdmin):

# 	fieldsets = [
# 		("Details", {'fields': ['album_name', 'artist_name', 'release_date', 'genre', 'is_single']}),
# 		("Content", {'fields': ['album_description', 'album_slug']})
# 	]

# 	formfield_overrides = {
# 		models.TextField : {'widget' : TinyMCE()}
# 	}

# class ArtistAdmin(admin.ModelAdmin):

# 	fieldsets = [
# 		("Details", {'fields': ['artist_name', 'artist_age', 'label_name']}),
# 		("Content", {'fields': ['artist_description']})
# 	]

# 	formfield_overrides = {
# 		models.TextField : {'widget' : TinyMCE()}
# 	}


admin.site.register(AlbumRating)
admin.site.register(TrackRating)
admin.site.register(Genre)
admin.site.register(Artist)
# admin.site.register(Album, AlbumAdmin)
admin.site.register(Album)
admin.site.register(Track)
