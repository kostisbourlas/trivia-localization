# This file will be used to import interfaces from other modules and map them
# into new methods that will be used strictly by this module

from typing import Set

from trivia_client import interface as trivia_interface
from transifex_client import interface as transifex_interface


class TriviaAPI:
    @staticmethod
    def get_trivias(categories: Set[str]) -> list[dict]:
        return trivia_interface.get_trivias_by_categories(categories)


class TransifexAPI:
    @staticmethod
    def create_resource(name: str) -> dict:
        return transifex_interface.create_resource(name)

    @staticmethod
    def get_all_resources() -> dict:
        return transifex_interface.get_all_resources()

    @staticmethod
    def upload_file_to_resource(file, filename: str, resource: str) -> dict:
        return transifex_interface.upload_file_to_resource(
            file, filename, resource
        )
