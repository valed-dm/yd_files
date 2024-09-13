"""
URLs for the yafiles app.

This module defines URL patterns for the yafiles application, mapping URLs to
view functions for handling Yandex Disk interactions, file management, and
bulk downloads.

URLs:
- ``/``: yandex_disk_view - Form to input Yandex Disk public link.
- ``/files/``: file_list_view - List view of all files and top-level folders.
- ``/files/<int:file_id>/``: file_detail_view - Detail view for a specific file.
- ``/folder/<path:folder_path>/``: folder_detail - Detail view for a specific folder.
- ``/files/download/``: bulk_download_view - Bulk download selected files as a ZIP
    archive.
"""

from django.urls import path

from . import views

app_name = "yafiles"
urlpatterns = [
    path("", views.yandex_disk_view, name="yandex_disk_form"),
    path("files/", views.file_list_view, name="file_list"),
    path("files/<int:file_id>/", views.file_detail_view, name="file_detail"),
    path("folder/<path:folder_path>/", views.folder_detail, name="folder_detail"),
    path("files/download/", views.bulk_download_view, name="bulk_download"),
]
