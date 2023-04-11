# The file maps all the relevant Trivia APIs.
import asyncio
from typing import List, Set

import aiohttp

from trivia_client.cache import AbstractCache
from trivia_client.exceptions import EmptyCategoryListError
from trivia_client.utils import (
    get_category_ids_by_names,
    call_url_for_each_category_async,
    get_results_from_responses,
    call_url_get
)


TRIVIA_API_TRIVIAS_URL: str = "https://opentdb.com/api.php"
TRIVIA_API_CATEGORIES_URL: str = "https://opentdb.com/api_category.php"
TRIVIA_CATEGORIES_KEY: str = "trivia_categories"
TRIVIA_RESULT_SIZE: int = 20


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
        try:
            responses: list = asyncio.run(
                call_url_for_each_category_async(
                    base_url=f"{TRIVIA_API_TRIVIAS_URL}?amount={TRIVIA_RESULT_SIZE}",
                    category_ids=category_ids
                )
            )
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return []

        trivias = get_results_from_responses(responses)
        return trivias

    def _get_categories(self):
        if self.cache:
            if not self.cache.get(TRIVIA_API_CATEGORIES_URL):
                response = call_url_get(TRIVIA_API_CATEGORIES_URL)
                self.cache.set(key=TRIVIA_API_CATEGORIES_URL, value=response)

            categories = self.cache.get(TRIVIA_API_CATEGORIES_URL)
        else:
            categories = call_url_get(TRIVIA_API_CATEGORIES_URL)

        return categories
