import requests


def slugify_string(string: str):
    return string.lower().replace(' ', '-')


def call_url_post(url: str, data: dict, headers: dict) -> dict:
    response = requests.post(url, json=data, headers=headers).json()
    return response
