"""Utils helpers module"""

import requests
from django.db import IntegrityError

from yd_files.yafiles.models import File
from yd_files.yafiles.models import Preview


def fetch_yandex_disk_content(link: str, folder_path: str = "") -> dict | None:
    """
        Fetches the content of a Yandex Disk folder or file.

        Args:
            link (str): The public link to the Yandex Disk.
            folder_path (str, optional): The path within the public link.
            Defaults to an empty string.

        Returns:
            Optional[Dict]: JSON response with the file structure if successful,
            else None.
        """
    api_url = "https://cloud-api.yandex.net/v1/disk/public/resources"
    req_url = f"{api_url}?public_key={link}&path={folder_path}"
    response = requests.get(req_url)
    if response.status_code == 200:
        return response.json()  # JSON response with the file structure
    return None  # Handle error cases


def save_file_and_previews(file_data_list: list[dict], public_link: str) -> None:
    """
        Saves file data and its associated previews to the database.

        Args:
            file_data_list (List[Dict]): List of file data dictionaries.
            public_link (str): The public link associated with the files.

        Returns:
            None
        """
    for file_data in file_data_list:
        try:
            # Attempt to create the file entry
            file_obj, created = File.objects.get_or_create(
                type=file_data.get("type", "type_not_available"),
                mime_type=file_data.get("mime_type", "mime_type_not_available"),
                name=file_data.get("name", None),
                path=file_data.get("path", None),
                file_url=file_data.get("file", "file_url_not_available"),
                public_link=public_link,
                size=file_data.get("size", 0),
                created=file_data.get("created", None),
                modified=file_data.get("modified", None),
            )

            # If the file was created, bulk create previews
            if created:
                previews_to_create = [
                    Preview(
                        file=file_obj,
                        size_name=preview["name"],
                        preview_url=preview["url"],
                    )
                    for preview in file_data.get("sizes", [])
                ]

                if previews_to_create:
                    Preview.objects.bulk_create(previews_to_create)

        except IntegrityError:
            pass


def download_file(public_link: str, path: str) -> bytes | None:
    """
        Downloads a file from Yandex Disk.

        Args:
            public_link (str): The public link to the Yandex Disk.
            path (str): The path to the file within the public link.

        Returns:
            Optional[bytes]: The file content if successful, else None.
        """
    api_url = "https://cloud-api.yandex.net/v1/disk/public/resources/download"
    params = {"public_key": public_link, "path": path}

    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        download_url = response.json()["href"]
        file_response = requests.get(download_url)
        if file_response.status_code == 200:
            return file_response.content
    return None  # Return None if download fails
