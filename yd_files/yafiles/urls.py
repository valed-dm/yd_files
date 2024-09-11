"""URLs for the yafiles app."""
from django.urls import path
from django.views.generic import TemplateView

app_name = "yafiles"
urlpatterns = [
    # ex: /files/
    path("", TemplateView.as_view(template_name="yafiles/files.html"), name="files"),
]
