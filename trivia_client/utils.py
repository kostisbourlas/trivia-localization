from typing import List, Set


def get_category_ids_by_names(
    categories: List[dict], names: Set[str]
) -> Set[int]:
    matching_ids: Set = set()
    for category in categories:
        if category["name"] in names:
            matching_ids.add(category["id"])

    return matching_ids
