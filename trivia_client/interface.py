# This is the interface that will be exposed publicly to the other modules.

from typing import List, Set

from trivia_client.cache import DictCache
from trivia_client.trivia_client import TriviaClient


DICT_CACHE = DictCache()


def get_trivias_by_categories(categories: Set[str] = None) -> List[dict]:
    client = TriviaClient(cache=DICT_CACHE)
    trivias: List[dict] = client.get_trivias_by_categories(categories)

    return trivias
