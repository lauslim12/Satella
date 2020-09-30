#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Imports
import argparse
import csv
import json
import math
import requests
import pprint  # DEBUG purposes only!
from datetime import datetime
from random import randint, choice

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

# Argument Parser
parser = argparse.ArgumentParser(
    description="Satella (version {}) is a program that helps you get your favorite characters via a personalized algorithm. Contribute to the project by contacting @lauslim12 on GitHub!".format(__version__),
    epilog='Please enjoy this automated program! If you have any issues or have any suggestions, please contact @lauslim12 at GitHub!')
parser.add_argument('-i', '--id', help='The anime ID that you want to query, but be warned that if you try to query by ID, then it is impossible to query by the year',
                    dest='specified_anime_id', type=int)
parser.add_argument('-y', '--year', help='The year to search for the animes',
                    dest='year', default=datetime.now().year, type=int)
parser.add_argument('-s',
                    '--season', help='The season to search for the animes. Can be combined with --year for better filtering', dest='season_name', choices=['SPRING', 'SUMMER', 'FALL', 'WINTER'], type=str)
parser.add_argument('-gf',
                    '--gender-filter', help='To disable exception being thrown if the character found is a male character', dest='male_filter', choices=['TRUE', 'FALSE'], type=str, default='TRUE')
parser.add_argument('-nf', '--none-filter', help='To disable exception being thrown if the character found is of unknown gender',
                    dest='none_filter', choices=['TRUE', 'FALSE'], type=str, default='FALSE')

args = parser.parse_args()


# Intentionally made public for easier data handling. We do not need any encapsulation in this part, as all the data is freely available.
class Data:
    def __init__(self):
        # Main
        self.characters = {}
        self.character = {}
        self.anime_id = 0
        self.anime_name = None
        self.page = {}
        self.contains_supporting = True
        self.page_to_take = 0
        self.character_type = 0
        self.predicted_gender = 0
        self.predicted_probability = 0
        self.number_of_main_characters = 0
        self.number_of_supporting_characters = 0
        self.number_of_main_characters_pages = 0
        self.number_of_supporting_characters_pages = 0
        self.main_characters = {}
        self.supporting_characters = {}

        # Utilities
        self.api_calls = 0
        self.max_pages = 0
        self.current_page = 0

    # BUG: Very redundant.
    def free_resources(self):
        self.characters = {}
        self.character = {}
        self.anime_id = 0
        self.anime_name = None
        self.page = {}
        self.contains_supporting = True
        self.page_to_take = 0
        self.character_type = 0
        self.predicted_gender = 0
        self.predicted_probability = 0
        self.number_of_main_characters = 0
        self.number_of_supporting_characters = 0
        self.number_of_main_characters_pages = 0
        self.number_of_supporting_characters_pages = 0
        self.main_characters = {}
        self.supporting_characters = {}

    def increment_api_calls(self):
        self.api_calls += 1

    def generate_number_of_main_characters(self, response):
        self.number_of_main_characters = response.get('data', None).get(
            'Page').get('media')[0].get('mainCharacters').get('pageInfo').get('total')


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
    data = Data()


if __name__ == "__main__":
    main()
