from django.urls import path

from .views import *

app_name = "accounts"

urlpatterns = [
    path('profile/edit', EditProfile, name="edit"),
    path('profile/documents', DocumentUploadProfile, name="profile-document"),
]
