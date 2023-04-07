# This file will be used to import interfaces from other modules and map them
# into new methods that will be used strictly by this module

from typing import Set, Generator

from trivia_client.interface import get_trivias_by_categories


def get_trivias(categories: Set[str]) -> Generator:
    for trivia in get_trivias_by_categories(categories):
        yield trivia
