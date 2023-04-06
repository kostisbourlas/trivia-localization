# This is the interface that will be used publicly from the other modules.

from typing import List

from trivia_client.trivia_client import TriviaClient


def get_trivias(categories: List[str] = None) -> List[dict]:
    client = TriviaClient(categories)
    trivias: List[dict] = client.retrieve_trivias()

    return trivias
