import html
import json
import os
import time
import uuid
import requests

from typing import Tuple, Set, Optional, Any, Callable, Union

from django.conf import settings

from localization.exceptions import NonPositiveNumberError
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


def remove_files(filepath: str) -> bool:
    try:
        os.remove(filepath)
    except FileNotFoundError:
        return False
    return True


def category_exists_in_resources(
    category: str, resources: Set[Resource]
) -> bool:
    for resource in resources:
        if resource.name == category:
            return True
    return False


def get_resource_from_storage(
    category: str, storage: Set[Resource]
) -> Optional[Resource]:
    for resource in storage:
        if resource.name == category:
            return resource


def get_dict_path(dictionary: dict, dict_path: str) -> Any:
    for item in dict_path.split("/"):
        dictionary = dictionary[item]
    return dictionary


def call_url_with_polling(
    call_method: Callable, retries: int, dict_path: str, message: str
) -> dict:
    for _ in range(retries):
        response = call_method()
        if get_dict_path(response, dict_path) == message:
            return response
        time.sleep(1)
    return {}


def call_url_with_retry(
    call_method: Callable, retries: int, error_codes: Set[int]
) -> Union[dict, requests.HTTPError]:
    if retries <= 0:
        raise NonPositiveNumberError

    backoff: int = 1
    while retries > 0:
        try:
            response: dict = call_method()
            return response
        except requests.HTTPError as e:
            retries -= 1
            for error_code in error_codes:
                if e.response.status_code == error_code:
                    time.sleep(backoff)
                    backoff *= 2
                    continue
            raise e


def construct_trivia_format(trivia: dict) -> dict:
    prefix: str = create_random_prefix()
    trivia_format = {
        f"{prefix}question": trivia.get("question"),
        f"{prefix}correct_answer": trivia.get("correct_answer"),
    }

    for index, answer in enumerate(trivia.get("incorrect_answers")):
        trivia_format.update({f"{prefix}incorrect_answer_{index}": answer})

    return trivia_format


def decode_dict_values(dictionary: dict) -> dict:
    for key, value in dictionary.items():
        if isinstance(value, str):
            decoded_value = decode_string(value)
            dictionary[key] = decoded_value
    return dictionary


def decode_string(string: str) -> str:
    return html.unescape(string)
