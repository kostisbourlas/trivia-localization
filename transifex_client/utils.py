import re

import requests


def slugify_string(string: str) -> str:
    string = string.lower().replace(' ', '-')
    string = re.sub(r'[^\w-]', '', string)
    return string


def call_url_post(url: str, data: dict, headers: dict) -> dict:
    response = requests.post(url, json=data, headers=headers).json()
    return response
