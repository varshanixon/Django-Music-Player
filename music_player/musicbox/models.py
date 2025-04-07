from random import randint

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


# Custom User Model
class User(AbstractUser):
    phone = models.CharField(max_length=15, unique=False)
    dob = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=4, null=True)

    def generate_otp(self):
        self.otp = str(randint(1000, 9999))
        self.save()
        print(f"Generated otp is {self.otp}")

    def __str__(self):
        return self.username


# Artist Model
class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Album Model
class Album(models.Model):
    title = models.CharField(max_length=100)
    artist_object = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="albums"
    )
    release_date = models.DateField()
    cover_photo = models.ImageField(upload_to="albumcovers", null=True, blank=True)

    def __str__(self):
        return self.title


# Genre Model
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Song Track Model
class SongTrack(models.Model):
    title = models.CharField(max_length=100)
    artist_object = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="tracks_artist"
    )
    album_object = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name="tracks_album",
        blank=True,
        null=True,
    )
    duration = models.DurationField()
    release_date = models.DateField()
    genre_objects = models.ManyToManyField(Genre)
    audio_file = models.FileField(upload_to="songtracks", blank=False, null=False)
    is_single = models.BooleanField(default=False)
    cover_photo = models.ImageField(upload_to="singlescover", blank=True, null=True)

    def __str__(self):
        return self.title


# Playlist Model
class Playlist(models.Model):
    name = models.CharField(max_length=100)
    user_object = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="playlists"
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    VISIBILITY_OPTIONS = (
        ("private", "Private"),
        ("public", "Public"),
    )
    visibility = models.CharField(
        max_length=50, choices=VISIBILITY_OPTIONS, default="private"
    )
    songtrack_objects = models.ManyToManyField(SongTrack)
    cover_image = models.ImageField(upload_to="playlistcovers", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    play_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


# LikedSongs Model
class LikedSong(models.Model):
    user_object = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="liked_songs"
    )
    songtrack_objects = models.ForeignKey(SongTrack, on_delete=models.CASCADE)
    liked_date = models.DateTimeField(auto_now_add=True)
