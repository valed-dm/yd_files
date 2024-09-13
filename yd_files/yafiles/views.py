"""Views module"""

import zipfile
from io import BytesIO
from urllib.parse import quote

from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import YandexDiskLinkForm
from .models import File
from .utils import download_file
from .utils import fetch_yandex_disk_content
from .utils import save_file_and_previews


def yandex_disk_view(request) -> HttpResponse:
    """
        Handles the form submission to fetch Yandex Disk data and store it in the session.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: Redirect to the file list view or render the form if GET.
        """
    if request.method == "POST":
        form = YandexDiskLinkForm(request.POST)
        if form.is_valid():
            public_link = form.cleaned_data["public_link"]
            # Store the public link in the session
            request.session["public_link"] = public_link

            # Fetch Yandex Disk data
            files_data = fetch_yandex_disk_content(public_link)
            if files_data:
                items = files_data.get("_embedded", {}).get("items", [])
                save_file_and_previews(file_data_list=items, public_link=public_link)
                return HttpResponseRedirect("files")
    else:
        form = YandexDiskLinkForm()

    return render(request, "yafiles/yandex_disk_form.html", {"form": form})


def file_list_view(request) -> HttpResponse:
    """
        Displays a list of files and top-level folders.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: Rendered file list and folder view.
        """
    public_link = request.session.get("public_link")

    # Get all folders (type='dir')
    all_folders = (File.objects
                   .filter(public_link=public_link, type="dir")
                   .values_list("path", flat=True))

    # Build exclusion criteria for enclosed folders
    folders_exclude_criteria = Q()
    for folder_path in all_folders:
        folders_exclude_criteria |= Q(path__startswith=folder_path + "/")

    # Fetch top-level folders only (those not enclosed in other folders)
    top_level_folders = (File.objects
                         .filter(public_link=public_link, type="dir")
                         .exclude(folders_exclude_criteria))

    # Build exclusion criteria for files in folders
    files_exclude_criteria = Q()
    for folder_path in all_folders:
        files_exclude_criteria |= Q(path__startswith=folder_path)

    # Fetch all files from the database and their previews
    files = File.objects.filter(public_link=public_link).exclude(files_exclude_criteria)
    return render(
        request,
        "yafiles/file_list.html",
        {"files": files, "folders": top_level_folders},
    )


def file_detail_view(request, file_id: int) -> HttpResponse:
    """
        Displays detailed information for a specific file.

        Args:
            request (HttpRequest): The request object.
            file_id (int): The ID of the file.

        Returns:
            HttpResponse: Rendered file detail view.
        """
    file = File.objects.get(id=file_id)
    previews = file.previews.all()
    return render(
        request,
        "yafiles/file_detail.html",
        {"file": file, "previews": previews},
    )


def folder_detail(request, folder_path: str) -> HttpResponse:
    """
        Displays the contents of a specific folder.

        Args:
            request (HttpRequest): The request object.
            folder_path (str): The path of the folder.

        Returns:
            HttpResponse: Rendered folder detail view or error if folder not found.
        """
    folder_path = "/" + folder_path
    public_link = request.session.get("public_link")
    folder_path_encoded = quote(folder_path)

    folder_files_data = fetch_yandex_disk_content(
        link=public_link,
        folder_path=folder_path_encoded,
    )

    folder_files_data = folder_files_data.get("_embedded", {})
    if folder_files_data and "items" in folder_files_data:
        items = folder_files_data.get("items", [])
        save_file_and_previews(file_data_list=items, public_link=public_link)

        # Filter files from the database by folder path
        files = (File.objects.filter(path__startswith=folder_path))
        return render(
            request,
            "yafiles/folder_detail.html",
            {"files": files, "folder_path": folder_path},
        )

    # Handle error (e.g., folder not found)
    return HttpResponseNotFound("Folder not found.")


def bulk_download_view(request) -> HttpResponse:
    """
       Handles bulk download of selected files as a ZIP archive.

       Args:
           request (HttpRequest): The request object.

       Returns:
           HttpResponse: ZIP file download response or error if no files selected.
       """
    if request.method == "POST":
        selected_file_ids = request.POST.getlist("selected_files")
        files_to_download = File.objects.filter(id__in=selected_file_ids)

        # Create an in-memory ZIP file
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for file in files_to_download:
                file_content = download_file(
                    public_link=file.public_link,
                    path=file.path,
                )
                zip_file.writestr(file.name, file_content)

        # Set the HTTP response headers
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=selected_files.zip"

        return response

    return HttpResponse("No files selected")
