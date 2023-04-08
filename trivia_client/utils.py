from typing import List, Set

import requests


def get_category_ids_by_names(
    categories: List[dict], names: Set[str]
) -> Set[int]:
    matching_ids: Set = set()
    for category in categories:
        if category["name"] in names:
            matching_ids.add(category["id"])

    return matching_ids


def call_url(url: str) -> dict:
    response = requests.get(url).json()
    return response
