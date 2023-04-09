from typing import Dict, Tuple

from localization.interface import upload_file_to_resource
from localization.utils import create_random_prefix, remove_files


def construct_trivia_format(trivia: dict) -> dict:
    prefix: str = create_random_prefix()
    trivia_format = {
        f"{prefix}question": trivia.get("question"),
        f"{prefix}correct_answer": trivia.get("correct_answer"),
    }

    for index, answer in enumerate(trivia.get("incorrect_answers")):
        trivia_format.update({f"{prefix}incorrect_answer_{index}": answer})

    return trivia_format


def upload_files_to_resources(mapper: Dict[str, Tuple]):
    for resource, file_details in mapper.items():
        with open(file_details[0], 'rb') as file:
            upload_file_to_resource(file, file_details[1], resource)
            _ = remove_files(file_details[0])
