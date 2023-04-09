import json
import os
import uuid
from typing import Tuple, Set

from django.conf import settings

from localization.objects import Resource


def create_random_prefix() -> str:
    # Generate a unique UUID prefix
    return f"q{uuid.uuid4().hex}_"


def append_data_to_file(data: dict, filename: str) -> Tuple[str, str]:
    filepath: str = f"{settings.UPLOADING_FILES_PATH}/{filename}"

    try:
        with open(filepath, "r") as file:
            file_data = json.load(file)
    except FileNotFoundError:
        file_data = {}

    file_data.update(data)

    with open(filepath, "a") as file:
        file.seek(0)
        file.truncate()
        json.dump(file_data, file)

    return filepath, filename


def remove_files(filepath: str) -> True:
    os.remove(filepath)
    return True


def category_exists_in_resources(
    category: str, resources: Set[Resource]
) -> bool:
    for resource in resources:
        if resource.name == category:
            return True
    return False
