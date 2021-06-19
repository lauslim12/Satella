#!usr/bin/env/python3
# -*- coding: utf-8 -*-
import asyncio
import json
from typing import Any, Dict

import aiohttp

from constants import ANILIST_API_URL, GRAPHQL_QUERY


async def fetch_anime_data(variables: Dict[str, Any]):
    request_body = {
        "query": GRAPHQL_QUERY,
        "variables": variables,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(ANILIST_API_URL, json=request_body) as response:
            return await response.json()


async def request():
    result = await fetch_anime_data({"year": 2021, "page": 6})
    print(json.dumps(result, indent=2, ensure_ascii=False))


async def main():
    await request()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
