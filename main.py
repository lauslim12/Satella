#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Imports
import math
from random import randint

# Metadata
__author__ = "Nicholas Dwiarto Wirasbawa"
__copyright__ = "Copyright 2020, Nicholas Dwiarto Wirasbawa"
__credits__ = "Nicholas Dwiarto Wirasbawa"

__license__ = "BSD-3 Revised"
__version__ = "1.0.0"
__maintainer__ = "Nicholas Dwiarto Wirasbawa"
__email__ = "nicholasdwiarto@yahoo.com"
__status__ = "Prototype"

# Constants
API_MAX_CALL_PER_PROGRAM = 25  # max is 90, but I'm not pushing my luck.
MAX_ANIME_PER_YEAR_ASSUMPTION = 400
ANILIST_API_URL = "https://graphql.anilist.co"
GENDERIZE_API_URL = "https://api.genderize.io"
GRAPHQL_QUERY = '''
query ($year: Int, $page: Int, $id: Int, $currentMainCharacterPage: Int, $currentSupportingCharacterPage: Int, $seasonName: MediaSeason) {
    Page(page: $page, perPage: 1) {
        pageInfo {
            total
            currentPage
            lastPage
        }
        media(id: $id, season: $seasonName, seasonYear: $year, type: ANIME, sort: FAVOURITES_DESC) {
            id
            seasonYear
            favourites
            title {
                userPreferred
            }
            mainCharacters: characters(sort: FAVOURITES_DESC, role: MAIN, page: $currentMainCharacterPage) {
                pageInfo {
                    total
                    currentPage
                    lastPage
                }
                nodes {
                    id
                    name {
                        first
                        last
                        full
                        native
                    }
                    favourites
                }
            }
            supportingCharacters: characters(sort: FAVOURITES_DESC, role: SUPPORTING, page: $currentSupportingCharacterPage) {
                pageInfo {
                    total
                    currentPage
                    lastPage
                }
                nodes {
                    id
                    name {
                        first
                        last
                        full
                        native
                    }
                    favourites
                }
            }
        }
    }
}
'''


class MaxCallsReachedError(Exception):
    def __init__(self):
        self.message = "You have already reached your max calls for this session! Please restart the program!"


def generate_weighted_random(max_pages=MAX_ANIME_PER_YEAR_ASSUMPTION):
    # We want the random number to be 85% biased towards upper numbers (first 10% of total / max pages, ceiled or rounded up).
    # Method: Random variates with Inverse CDF Method.
    print("Generating a new biased ID with max randomized number:", max_pages)
    number = randint(1, 100)

    # If the data is too small (1), we will not use the below function.
    # Usually, the reason this is used is because we queried by ID (if we search for an anime, the result will always be one page / title only).
    if max_pages == 1:
        return 1

    top_anime_pages = math.ceil(max_pages * 0.1)

    print("Top anime pages ranges from page 1 to page {}!".format(top_anime_pages))

    if number <= 85:
        return randint(1, top_anime_pages)
    else:
        return randint(top_anime_pages + 1, max_pages)


def check_if_already_at_the_limit(data):
    if data.api_calls >= API_MAX_CALL_PER_PROGRAM:
        raise MaxCallsReachedError()

    return None


def main():
    pass


if __name__ == "__main__":
    main()
