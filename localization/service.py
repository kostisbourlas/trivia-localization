from django.conf import settings

from localization.interface import create_resource
from localization.utils import create_random_prefix, append_data_to_file


def construct_trivia_format(trivia: dict) -> dict:
    prefix: str = create_random_prefix()
    trivia_format = {
        f"{prefix}question": trivia.get("question"),
        f"{prefix}correct_answer": trivia.get("correct_answer"),
    }

    for index, answer in enumerate(trivia.get("incorrect_answers")):
        trivia_format.update({f"{prefix}incorrect_answer_{index}": answer})

    return trivia_format


def localize_trivia(trivia: dict):
    trivia_data: dict = construct_trivia_format(trivia)
    append_data_to_file(
        trivia_data,
        f"{trivia.get('category')}{settings.TRIVIA_FILES_SUFFIX}.json"
    )
    _ = create_resource(trivia.get("category"))
