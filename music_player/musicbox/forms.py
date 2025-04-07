from django import forms
from django.contrib.auth.forms import UserCreationForm

from musicbox.models import Playlist, SongTrack, User


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "dob",
            "phone",
            "email",
            "password1",
            "password2",
        ]


class OtpVerifyForm(forms.Form):
    otp = forms.CharField(max_length=4)


class SignInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class CreatePlaylistForm(forms.ModelForm):

    class Meta:
        model = Playlist
        fields = ["name", "cover_image", "visibility"]



class AddSongToPlaylistForm(forms.Form):

    songs = forms.ModelMultipleChoiceField(
        queryset=SongTrack.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        playlist = kwargs.pop("playlist", None)
        super().__init__(*args, **kwargs)

        if playlist:
            existing_songs = playlist.songtrack_objects.all()
            self.fields["songs"].queryset = SongTrack.objects.exclude(
                id__in=existing_songs
            )
