from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from musicbox.models import Album, Artist, Genre, LikedSong, Playlist, SongTrack, User

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Genre)
admin.site.register(Playlist)
admin.site.register(LikedSong)
admin.site.register(SongTrack)
