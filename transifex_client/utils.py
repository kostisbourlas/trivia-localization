import re

import requests

from transifex_client import settings


def slugify_string(string: str) -> str:
    string = string.lower().replace(' ', '-')
    string = re.sub(r'[^\w-]', '', string)
    return string


def call_url_post(url: str, data: dict, headers: dict, files: dict = None) -> dict:
    response = requests.post(url, json=data, headers=headers, files=files)
    return response.json()


def call_url_post_with_files(url, files, headers, payload):
    response = requests.post(
        url, headers=headers, data=payload, files=files
    )
    return response.json()
