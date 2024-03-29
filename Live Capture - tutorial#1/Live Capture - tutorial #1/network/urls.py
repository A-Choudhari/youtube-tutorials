
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("image", views.live_capture_view, name="image"),
    path("audio", views.live_capture_audio, name="audio"),
]
