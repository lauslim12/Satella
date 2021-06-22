"""API helpers to help with Genderize API."""

import asyncio

import aiohttp
from aiohttp.client import ClientSession

from constants import GENDERIZE_API_URL
from datatypes import GenderizeResponse
from utilities import valid_response


async def fetch_genderize(session: ClientSession, parameter: str) -> GenderizeResponse:
    """Fetches data asynchronously from Genderize API."""
    formatted_url = f"{GENDERIZE_API_URL}/{parameter}"

    async with session.get(formatted_url) as response:
        if valid_response(response, "Genderize"):
            return await response.json()


async def fetch_genders_from_genderize(
    parameters: list[str],
) -> list[GenderizeResponse]:
    """Prepare to do several parallel requests to the Genderize API."""
    tasks = []

    async with aiohttp.ClientSession() as session:
        for parameter in parameters:
            task = asyncio.create_task(fetch_genderize(session, parameter))
            tasks.append(task)

        # alternative to 'Promise.all' in JavaScript
        responses: list[GenderizeResponse] = await asyncio.gather(*tasks)
        return responses


def is_male_character(gender: GenderizeResponse) -> bool:
    """Checks whether the character is male or not."""
    if gender["gender"] == "male" and gender["probability"] > 0.5:
        return True

    return False


def is_female_character(gender: GenderizeResponse) -> bool:
    """Checks whether the character is female or not."""
    if gender["gender"] == "female" and gender["probability"] > 0.5:
        return True

    return False
