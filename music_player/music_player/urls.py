"""
URL configuration for music_player project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from musicbox import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("verify-otp/", views.OtpVerifyView.as_view(), name="otp-verify"),
    path("signin/", views.SignInView.as_view(), name="signin"),
    path("signout/", views.SignOutView.as_view(), name="signout"),
    path("", views.IndexView.as_view(), name="index"),
    path(
        "playlist/create/", views.PlaylistCreateView.as_view(), name="playlist-create"
    ),
    path(
        "playlist/<int:pk>/add-songs/",
        views.PlaylistAddSongsView.as_view(),
        name="playlist-add-songs",
    ),
    path("playlist/list/", views.PlaylistListView.as_view(), name="playlist-list"),
    path(
        "playlist/<int:pk>/detail/",
        views.PlaylistDetailView.as_view(),
        name="playlist-details",
    ),
    path(
        "playlist/<int:pk>/delete/",
        views.PlaylistDeleteView.as_view(),
        name="playlist-delete",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
