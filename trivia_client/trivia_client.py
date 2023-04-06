# The file maps all the relevant Trivia APIs.

from typing import List

from trivia_client.exceptions import EmptyCategoryListError


class TriviaClient:
    def __init__(self, categories: List[str] = None):
        if categories is None:
            categories = []

        self.categories = categories

    def retrieve_trivias(self) -> List[dict]:
        if not self.categories:
            raise EmptyCategoryListError

        return [{}, {}, {}]
