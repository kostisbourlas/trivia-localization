import json
import uuid

from django.conf import settings


def create_random_prefix() -> str:
    # Generate a unique UUID prefix
    return f"q{uuid.uuid4().hex}_"


def append_data_to_file(data: dict, filename: str):
    file_path: str = f"{settings.UPLOADING_FILES_PATH}/{filename}"

    try:
        with open(file_path, 'r') as file:
            file_data = json.load(file)
    except FileNotFoundError:
        file_data = {}

    file_data.update(data)

    with open(file_path, "a") as file:
        file.seek(0)
        file.truncate()
        json.dump(file_data, file)
