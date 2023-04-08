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


def call_url_for_each_category(base_url: str, category_ids: Set[int]):
    trivias: List[dict] = []
    for category_id in category_ids:
        # TODO: Make use of async request
        response = call_url(f"{base_url}&category={category_id}")
        trivias.extend(response.get("results"))

    return trivias
