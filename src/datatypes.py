"""This file will store the 'types' of any unique dictionaries in the program."""

from __future__ import annotations

from typing import Literal, TypedDict


class AniListRawResponse(TypedDict):
    """Raw AniList response."""

    data: AniListParsedResponse


class AniListParsedResponse(TypedDict):
    """AniList response that has been parsed: starting from "Page" key."""

    pageInfo: PageInfo
    media: list[Media]


class Character(TypedDict):
    """Type for a character in a parsed response."""

    id: int
    name: CharacterName
    favourites: str


class CharacterName(TypedDict):
    """Character name object in the response."""

    first: str
    last: str
    full: str
    native: str


class CharacterInformation(TypedDict):
    """Character information in the response."""

    pageInfo: PageInfo
    nodes: list[Character]


class Data(TypedDict):
    """Data (before being processed) in the program."""

    id: int
    name: CharacterName
    favourites: int
    anime: str


class GenderizeResponse(TypedDict):
    """Raw Genderize API response."""

    name: str
    gender: Literal["male", "female"]
    probability: float
    count: int
    country_id: str


class Media(TypedDict):
    """Media object from AniList API."""

    id: int
    seasonYear: int
    favourites: int
    title: Title
    mainCharacters: CharacterInformation
    supportingCharacters: CharacterInformation


class PageInfo(TypedDict):
    """PageInfo object from AniList API."""

    total: int
    currentPage: int
    lastPage: int


class ProcessedData(TypedDict):
    """Processed data to be inserted to the CSV file."""

    character: Data
    gender: GenderizeResponse


class Title(TypedDict):
    """Title object from AniList API."""

    userPreferred: str
