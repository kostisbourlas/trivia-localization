import asyncio
from typing import List, Set

import aiohttp


def get_category_ids_by_names(
    categories: List[dict], names: Set[str]
) -> Set[int]:
    matching_ids: Set = set()
    for category in categories:
        if category["name"] in names:
            matching_ids.add(category["id"])

    return matching_ids


async def call_url_async(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as resp:
        response = await resp.json()
        return response


async def call_url_for_each_category_async(base_url: str, category_ids: Set[int]):
    tasks = []

    async with aiohttp.ClientSession() as session:
        for category_id in category_ids:
            tasks.append(
                asyncio.ensure_future(
                    call_url_async(session, f"{base_url}&category={category_id}")
                )
            )

        responses = await asyncio.gather(*tasks)

        trivias: List[dict] = []
        for resp in responses:
            trivias.extend(resp.get("results"))

    return trivias
