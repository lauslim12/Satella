"""API helpers to help parse and get the data."""
from typing import Any

import aiohttp

from constants import ANILIST_API_URL, GRAPHQL_QUERY
from datatypes import AniListRawResponse, Character, Media, PageInfo


async def fetch_from_anilist(variables: dict[str, Any]) -> AniListRawResponse:
    """This is to fetch data from the AniList API, asynchronously."""
    request_body = {"query": GRAPHQL_QUERY, "variables": variables}

    async with aiohttp.ClientSession() as session:
        async with session.post(ANILIST_API_URL, json=request_body) as response:
            return await response.json()


async def fetch_from_anilist_specific_page(
    anime_id: str, page: int
) -> AniListRawResponse:
    """This is to fetch the data from AniList, for a specific page."""
    variables = {
        "id": anime_id,
        "currentMainCharacterPage": page,
        "currentSupportingCharacterPage": page,
    }

    response = await fetch_from_anilist(variables)
    return response


def anime_media(raw_data: AniListRawResponse) -> Media:
    """Returns the media object from the API."""
    return raw_data["data"]["Page"]["media"][0]


def all_main_characters(raw_data: AniListRawResponse) -> list[Character]:
    """Returns all of the main characters from the data."""
    characters: list[Character] = anime_media(raw_data)["mainCharacters"]["nodes"]
    return characters


def all_supporting_characters(raw_data: AniListRawResponse) -> list[Character]:
    """Returns all of the supporting characters from the data."""
    characters: list[Character] = anime_media(raw_data)["supportingCharacters"]["nodes"]
    return characters


def anime_page_info(raw_data: AniListRawResponse) -> PageInfo:
    """Returns the media page info from the data."""
    return raw_data["data"]["Page"]["pageInfo"]


def main_characters_page_info(raw_data: AniListRawResponse) -> PageInfo:
    """Returns the main characters page info from the data."""
    return anime_media(raw_data)["mainCharacters"]["pageInfo"]


def supporting_characters_page_info(raw_data: AniListRawResponse) -> PageInfo:
    """Returns the supporting characters page info from the data."""
    return anime_media(raw_data)["supportingCharacters"]["pageInfo"]


def media_exists(raw_data: AniListRawResponse) -> bool:
    """Returns a boolean whether there is any media or not."""
    if raw_data["data"]["Page"]["media"]:
        return True

    return False
