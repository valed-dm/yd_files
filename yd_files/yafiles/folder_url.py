"""This module was used just for testing that URL now is properly encoded"""

from pprint import pprint

import requests


def fetch_yandex_disk_content(link, path):
    api_url = "https://cloud-api.yandex.net/v1/disk/public/resources"
    params = {"public_key": link, "path": path}

    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json()  # JSON response with the file structure
    return None  # Handle error cases


pprint(fetch_yandex_disk_content(
    link="https://disk.yandex.com/d/TKbB_n0bQm99GQ",
    path="%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%87%D0%B8%D0%BA%20Simple"
))
