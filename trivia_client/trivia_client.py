# The file maps all the relevant Trivia APIs.

from typing import List, Set

import requests

from trivia_client.cache import AbstractCache
from trivia_client.exceptions import EmptyCategoryListError
from trivia_client.utils import get_category_ids_by_names, call_url

TRIVIA_API_TRIVIAS: str = "https://opentdb.com/api.php"
TRIVIA_API_CATEGORIES: str = "https://opentdb.com/api_category.php"
TRIVIA_CATEGORIES_KEY: str = "trivia_categories"
TRIVIA_RESULT_SIZE: int = 1


class TriviaClient:
    def __init__(self, cache: AbstractCache = None):
        self.cache = cache

    def get_trivias_by_categories(self, categories: Set[str]) -> List[dict]:
        if not categories:
            raise EmptyCategoryListError

        category_list: List = self._get_categories().get(TRIVIA_CATEGORIES_KEY)

        trivias: List[dict] = []
        category_ids: Set[int] = get_category_ids_by_names(
            category_list, categories
        )
        self.call_url_for_each_category(category_ids, trivias)

        return trivias

    def call_url_for_each_category(self, category_ids, trivias):
        for category_id in category_ids:
            # TODO: Make use of async request
            response = call_url(
                f"{TRIVIA_API_TRIVIAS}?amount={TRIVIA_RESULT_SIZE}&category={category_id}"
            )
            trivias.extend(response.get("results"))

    def _get_categories(self):
        if self.cache:
            if not self.cache.get(TRIVIA_API_CATEGORIES):
                response = requests.get(TRIVIA_API_CATEGORIES)
                self.cache.set(key=TRIVIA_API_CATEGORIES, value=response.json())

            categories = self.cache.get(TRIVIA_API_CATEGORIES)
        else:
            categories = requests.get(TRIVIA_API_CATEGORIES).json()

        return categories
