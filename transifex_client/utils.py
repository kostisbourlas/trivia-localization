import re

import requests


def slugify_string(string: str) -> str:
    string = string.lower().replace(" ", "-")
    string = re.sub(r"[^\w-]", "", string)
    return string


def call_url_get(url: str, headers: dict):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def call_url_post(url: str, data: dict, headers: dict) -> dict:
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()


def call_url_post_with_files(url, files, headers, payload):
    response = requests.post(
        url, headers=headers, data=payload, files=files
    )
    response.raise_for_status()
    return response.json()
