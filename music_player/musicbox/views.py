# Standard library imports
from decouple import config
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

# Third party imports
from twilio.rest import Client

# Local application imports
from musicbox.forms import (
    AddSongToPlaylistForm,
    CreatePlaylistForm,
    OtpVerifyForm,
    SignInForm,
    SignUpForm,
)
from musicbox.models import Playlist, SongTrack, User

# Create your views here.

"""Initialize Twilio client using global credentials.    
    WARNING: These are sensitive values - always load from environment
    variables in production environments.
"""
TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NO = config("TWILIO_PHONE_NO")
USER_PHONE = config("USER_PHONE")


def send_otp_phone(user_object, user_phone):
    """To send otp to user's phone number.

    WARNING: Use the upgraded twilio account. If you are using trial account,
    change user_phone to your phone number.
    """

    user_object.generate_otp()

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        from_=TWILIO_PHONE_NO,
        body=f"Your one-time password is {user_object.otp}.",
        to=USER_PHONE,
    )

    # For debugging
    print(f"OTP sent successfully: {message.sid}")


class SignUpView(View):
    template_name = "signup.html"
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        form_instance = self.form_class
        return render(request, self.template_name, {"form": form_instance})

    def post(self, request, *args, **kwargs):
        form_instance = self.form_class(request.POST)

        if form_instance.is_valid():
            user_instance = form_instance.save(commit=False)
            user_instance.is_active = False
            user_instance.save()

            send_otp_phone(user_instance, user_instance.phone)
            return redirect("otp-verify")

        return render(request, self.template_name, {"form": form_instance})


class OtpVerifyView(View):
    template_name = "otpverify.html"
    form_class = OtpVerifyForm

    def get(self, request, *args, **kwargs):
        form_instance = self.form_class()
        return render(request, self.template_name, {"form": form_instance})

    def post(self, request, *args, **kwargs):
        otp = request.POST.get("otp")
        print(f"Recieved otp {otp}")

        try:
            user_object = User.objects.get(otp=otp)
            user_object.is_active = True
            user_object.is_verified = True
            user_object.otp = None
            user_object.save()

            messages.success(request, "OTP verified successfully!")
            return redirect("signin")

        except:
            messages.error(request, "Verification failed. Please try again.")
            return redirect("otp-verify")


class SignInView(View):
    form_class = SignInForm
    template_name = "signin.html"

    def get(self, request, *args, **kwargs):
        form_instance = self.form_class()
        return render(request, self.template_name, {"form": form_instance})

    def post(self, request, *args, **kwargs):
        form_instance = self.form_class(request.POST)

        if form_instance.is_valid():
            uname = form_instance.cleaned_data.get("username")
            pwd = form_instance.cleaned_data.get("password")
            user_object = authenticate(request, username=uname, password=pwd)

            if user_object:

                login(request, user_object)

                return redirect("index")

        return render(request, self.template_name, {"form": form_instance})


class SignOutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("signin")


class IndexView(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        songs = SongTrack.objects.all()
        return render(request, self.template_name, {"songs": songs})


class PlaylistCreateView(LoginRequiredMixin, View):
    login_url = "signin"
    redirect_field_name = "redirect_to"
    form_class = CreatePlaylistForm

    def post(self, request, *args, **kwargs):
        form_instance = self.form_class(request.POST, request.FILES)

        if form_instance.is_valid():
            playlist = form_instance.save(commit=False)
            playlist.user_object = request.user
            playlist.save()

            messages.success(request, "Playlist created successfully!")
            return redirect("playlist-list")

        for error in form_instance.errors.values():
            messages.error(request, error)
        return redirect("playlist-list")


class PlaylistDeleteView(LoginRequiredMixin, View):
    login_url = "signin"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        playlist_id = kwargs.get("pk")
        get_object_or_404(Playlist, user_object=request.user, id=playlist_id).delete()
        return redirect("playlist-list")


class PlaylistAddSongsView(LoginRequiredMixin, View):
    login_url = "signin"
    redirect_field_name = "redirect_to"
    template_name = "add-songs-playlist.html"
    form_class = AddSongToPlaylistForm

    def get(self, request, *args, **kwargs):
        playlist_id = kwargs.get("pk")
        playlist = get_object_or_404(Playlist, id=playlist_id, user_object=request.user)
        form_instance = self.form_class(playlist=playlist)
        return render(
            request, self.template_name, {"form": form_instance, "playlist": playlist}
        )

    def post(self, request, *args, **kwargs):
        playlist_id = kwargs.get("pk")
        playlist = get_object_or_404(Playlist, id=playlist_id, user_object=request.user)
        form_instance = self.form_class(request.POST, playlist=playlist)

        if form_instance.is_valid():
            selected_songs = form_instance.cleaned_data.get("songs")
            playlist.songtrack_objects.add(*selected_songs)

            messages.success(request, "Songs added to the playlist!")
            return redirect("playlist-details", pk=playlist_id)

        return render(
            request, self.template_name, {"form": form_instance, "playlist": playlist}
        )


class PlaylistDetailView(LoginRequiredMixin, View):
    login_url = "signin"
    redirect_field_name = "redirect_to"
    template_name = "detail-playlist.html"

    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        playlist = get_object_or_404(Playlist, id=id, user_object=request.user)
        return render(request, self.template_name, {"playlist": playlist})


# class RemoveSongsFromPlaylistView(View):


class PlaylistListView(LoginRequiredMixin, View):
    login_url = "signin"
    redirect_field_name = "redirect_to"
    template_name = "list-playlists.html"

    def get(self, request, *args, **kwargs):
        playlists = Playlist.objects.filter(user_object=request.user)
        return render(request, self.template_name, {"playlists": playlists})
