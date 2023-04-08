# The file maps all the relevant Trivia APIs.

from typing import List, Set

import requests

from trivia_client.cache import AbstractCache
from trivia_client.exceptions import EmptyCategoryListError
from trivia_client.utils import get_category_ids_by_names, call_url

TRIVIA_API_TRIVIAS_URL: str = "https://opentdb.com/api.php"
TRIVIA_API_CATEGORIES_URL: str = "https://opentdb.com/api_category.php"
TRIVIA_CATEGORIES_KEY: str = "trivia_categories"
TRIVIA_RESULT_SIZE: int = 1


class TriviaClient:
    def __init__(self, cache: AbstractCache = None):
        self.cache = cache

    def get_trivias_by_categories(self, categories: Set[str]) -> List[dict]:
        if not categories:
            raise EmptyCategoryListError

        category_list: List = self._get_categories().get(TRIVIA_CATEGORIES_KEY)

        category_ids: Set[int] = get_category_ids_by_names(
            category_list, categories
        )
        trivias: List[dict] = self.call_url_for_each_category(
            base_url=f"{TRIVIA_API_TRIVIAS_URL}?amount={TRIVIA_RESULT_SIZE}",
            category_ids=category_ids
        )

        return trivias

    def call_url_for_each_category(self, base_url: str, category_ids: Set[int]):
        trivias: List[dict] = []
        for category_id in category_ids:
            # TODO: Make use of async request
            response = call_url(f"{base_url}&category={category_id}")
            trivias.extend(response.get("results"))

        return trivias

    def _get_categories(self):
        if self.cache:
            if not self.cache.get(TRIVIA_API_CATEGORIES_URL):
                response = requests.get(TRIVIA_API_CATEGORIES_URL)
                self.cache.set(key=TRIVIA_API_CATEGORIES_URL, value=response.json())

            categories = self.cache.get(TRIVIA_API_CATEGORIES_URL)
        else:
            categories = requests.get(TRIVIA_API_CATEGORIES_URL).json()

        return categories
