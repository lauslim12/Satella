# BUG: If ID is placed, the 'generate_weighted_random' can fail. Look at line 100 and 285 (variable object and returned function). That is the cause of the bug.
# TODO DONE: Add argparser, change weighed algorithm to be 10% of the max page, disable gender checks (argparser), and add counter to prevent hoarding.
# TODO: Devise new algorithm step before looking checking -> first check all the total data in the current year. Store variable in the 'max_pages' variable.
# TODO: Implement the 'NoneCharacterError' exception.
# TODO: Also be able to check from manga.
# TODO: PyInstaller for executable files.
# TODO: CSV Name to constants -- add option to take from argument parser.
# TODO: clean.py to main.py with argument parser.

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


class MaxPageExceededError(Exception):
    def __init__(self):
        self.message = "The randomly generated number is higher than the max page! Retrying, this time with the maximum randomly generated number being the max available number in the query."


class NoMainCharactersError(Exception):
    def __init__(self):
        self.message = "There are no main characters for this anime! Fetching another data..."


class MaleCharacterError(Exception):
    def __init__(self):
        self.message = "The character is a male! Retrying from another anime..."


class NoCharacterError(Exception):
    def __init__(self):
        self.message = "The character is a None (undetected by the API)! Retrying from another anime..."


class DuplicateEntryError(Exception):
    def __init__(self):
        self.message = "There is a duplicate entry in the CSV file! Retrying with another anime..."


class MaxCallsReachedError(Exception):
    def __init__(self):
        self.message = "You have already reached your max calls for this session! Please restart the program!"


class NoMediaFoundError(Exception):
    def __init__(self, anime_id):
        self.message = "The media with ID {} was not found! Perhaps you have typed the wrong ID? Exiting program...".format(
            anime_id)


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


def check_maximum_page(data):
    pass


def fetch_data(data, current_page=0):
    # Print message for clarity.
    print("Current page of the present query:", current_page)

    # Increment API calls.
    data.increment_api_calls()
    print("Current API calls for this session:", data.api_calls)

    # Variables for the GraphQL.
    # Year is set to 2020, it can be easily set to be the wanted year.
    variables = {
        'year': args.year,
        'page': generate_weighted_random(MAX_ANIME_PER_YEAR_ASSUMPTION) if current_page == 0 else current_page,
    }

    # If there is an ID, append ID to the query.
    # If the user only places an ID, remove the year. It might cause several unwanted bugs (e.g. querying an anime whose year is not in 2020, resulting in a crash)
    # BUG: We should add an argument taken from the command line if we need to specifiy an ID and its year.
    # specified_anime_id = args.specified_anime_id if args.specified_anime_id is not None else None
    if args.specified_anime_id is not None:
        variables.update({'id': args.specified_anime_id})
        variables.pop('year')

    # If there is a season specified, append seasonName to the variable.
    # BUG: Same as above.
    # Season: SPRING, SUMMER, FALL, WINTER
    # season_name = None
    if args.season_name is not None:
        variables.update({'seasonName': args.season_name})

    # Body to be sent.
    request_body = {
        'query': GRAPHQL_QUERY,
        'variables': variables
    }

    # Print message for clarity.
    page_now_looking = variables.get('page')
    year_now_looking = variables.get('year')
    print("Attempting to get data from page {} of year {}...".format(
        page_now_looking, year_now_looking))

    # API POST call to the GraphQL API.
    response = requests.post(ANILIST_API_URL, json=request_body)
    response = response.json()

    # Shuffle through the results.
    data.max_pages = response['data']['Page']['pageInfo']['total']
    data.current_page = response['data']['Page']['pageInfo']['currentPage']

    # Precaution: If searching results in no data, raise an error.
    if data.max_pages <= 0:
        raise NoMediaFoundError(args.specified_anime_id)

    # If the current randomly generated page fails, retry query again with a randomly generated number whose maximum is the 'max_pages' variable.
    if data.max_pages < data.current_page:
        data.current_page = generate_weighted_random(data.max_pages)
        raise MaxPageExceededError()

    data.number_of_main_characters = response['data']['Page']['media'][0]['mainCharacters']['pageInfo']['total']
    data.number_of_supporting_characters = response['data']['Page'][
        'media'][0]['supportingCharacters']['pageInfo']['total']
    data.anime_id = response['data']['Page']['media'][0]['id']
    data.anime_name = response['data']['Page']['media'][0]['title']['userPreferred']

    # Print message for clarity.
    print("Attempting to take data from anime: {}... (ID: {})".format(
        data.anime_name, data.anime_id))

    # Check for empty objects.
    if data.number_of_main_characters <= 0:
        data.current_page = generate_weighted_random(data.max_pages)
        raise NoMainCharactersError()

    # Print the character generated.
    data.characters = response['data']['Page']['media'][0]

    # Check for empty supporting characters. Main characters cannot be empty, because it has passed the above check.
    if data.number_of_supporting_characters <= 0:
        data.contains_supporting = False
        return None

    return None


# 1 is 'Main' and 2 is 'Supporting'
def choose_characters(data):
    data.number_of_main_characters_pages = data.characters['mainCharacters']['pageInfo']['lastPage']
    data.number_of_supporting_characters_pages = data.characters[
        'supportingCharacters']['pageInfo']['lastPage']

    # Randomized integer to take data from a certain page.
    if data.contains_supporting is False:
        print("No supporting characters in this anime! All data taken will be from main characters!")

        # Randomly choose which page to take a character from.
        data.page_to_take = randint(1, data.number_of_main_characters_pages)

        # Instantly call the 'take_character' function.
        data.main_characters = data.characters['mainCharacters']['nodes']
        data.character_type = 1
        return None
    else:
        # Randomly choose (50% chance) whether to take data from a main character or a supporting character.
        choose_from_main = choice([True, False])

        if choose_from_main is True:
            # Randomly choose which page to take a character from.
            data.page_to_take = randint(
                1, data.number_of_main_characters_pages)
            data.main_characters = data.characters['mainCharacters']['nodes']
            data.character_type = 1
            return None

        # Randomly choose which page to take a character from.
        data.page_to_take = randint(
            1, data.number_of_supporting_characters_pages)
        data.supporting_characters = data.characters['supportingCharacters']['nodes']
        data.character_type = 2
        return None


def take_character(data):
    # Message to tells us what type of character that we are taking.
    if data.character_type == 1:
        print("Taking a main character from page {}!".format(data.page_to_take))
    else:
        print("Taking a supporting character from page {}!".format(data.page_to_take))

    # If the page is not one, then query again with the page to take a character from.
    if data.page_to_take != 1:
        # Increment API calls.
        data.increment_api_calls()
        print("Current API calls for this session:", data.api_calls)

        variables = {
            'id': data.anime_id,
            'currentMainCharacterPage': data.page_to_take if data.character_type == 1 else 1,
            'currentSupportingCharacterPage': data.page_to_take if data.character_type == 2 else 1
        }

        request_body = {
            'query': GRAPHQL_QUERY,
            'variables': variables
        }

        response = requests.post(ANILIST_API_URL, json=request_body)
        response = response.json()

        data.main_characters = response['data']['Page']['media'][0]['mainCharacters']['nodes']
        data.supporting_characters = response['data']['Page']['media'][0]['supportingCharacters']['nodes']

        # Take data randomly.
        if data.character_type == 1:
            data.character = choice(data.main_characters)
        else:
            data.character = choice(data.supporting_characters)
    else:
        # Take data randomly from available characters, depending on the character type.
        data_to_take = data.main_characters if data.character_type == 1 else data.supporting_characters
        data.character = choice(data_to_take)

    character_name = data.character['name']['full']
    print("Taken character {} from Anime ID: {} on date-time {}!".format(
        character_name, data.anime_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    return None


def determine_gender(data):
    # We also pass the main characters array to perform the second optional algorithm, which is if not female, then instead of reshuffling through the anime, we can simply increase the index by one, and if the index is full, check supporting characters.
    # Determine a character name.
    # If the first name is empty, then prepare to use the last name instead.
    character_name = data.character['name']['first'] if data.character[
        'name']['first'] != "" else data.character['name']['last']
    character_name = character_name.strip()
    formatted_genderize_api_url = "{}?name={}&country_id=JP".format(
        GENDERIZE_API_URL, character_name)

    response = requests.get(formatted_genderize_api_url)
    response = response.json()

    # Parse the output.
    data.predicted_gender = response['gender']
    data.predicted_probability = response['probability']

    # Print message for clarity.
    print("Character {} is a {} with the probability of {}% (using Japanese country code).".format(
        character_name, data.predicted_gender, data.predicted_probability * 100))

    # If female, no matter the probability, insert to CSV.
    # If male > 50%, reject.
    # If Null, another API call without the country code (some anime girls can have weird names)
    # If Null results in Null or Male (< 50%), insert to CSV.
    # BUG: Please use booleans, not strings.
    if data.predicted_gender == "male" and data.predicted_probability > 0.5 and args.male_filter == "TRUE":
        data.current_page = generate_weighted_random(data.max_pages)
        raise MaleCharacterError()

    if data.predicted_gender is None:
        formatted_genderize_api_url = "{}?name={}".format(
            GENDERIZE_API_URL, character_name)
        response = requests.get(formatted_genderize_api_url)
        response = response.json()

        data.predicted_gender = response['gender']
        data.predicted_probability = response['probability']

        # Print message for clarity.
        print("Character {} is a {} with the probability of {}% (no country code used).".format(
            character_name, data.predicted_gender, data.predicted_probability * 100))

        # BUG: Please use booleans, not strings.
        if data.predicted_gender == "male" and data.predicted_probability > 0.5 and args.male_filter == "TRUE":
            data.current_page = generate_weighted_random(data.max_pages)
            raise MaleCharacterError()

    return None


def write_to_csv(data):
    print(json.dumps(data.character, indent=2))
    # Parse the character dict into variables for easier typing.
    character_id = data.character['id']
    character_first_name = data.character['name']['first']
    character_last_name = data.character['name']['last']
    character_full_name = data.character['name']['full']
    character_favorites = data.character['favourites']
    date_taken = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check for duplicates first. If it contains duplicate, it will raise an exception.
    check_for_duplicate_entries(character_id, data)

    # BUG: This should have max_pages. Fix it when we modularize all the functions to main.
    # if is_duplicate is True:
    #     return False

    # Store the data into a CSV file.
    with open('data/suggestions.csv', 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([character_id, character_first_name, character_last_name, character_full_name,
                             character_favorites, data.predicted_gender, data.predicted_probability, data.anime_name, date_taken])

    print("Data successfully stored in CSV!")
    return True


def check_for_duplicate_entries(character_id, data):
    # Check for duplicates.
    with open('data/suggestions.csv', 'r', encoding='utf-8') as csv_file:
        if str(character_id) in csv_file.read():
            data.current_page = generate_weighted_random(data.max_pages)
            raise DuplicateEntryError()

        return False


def main():
    data = Data()

    while True:
        try:
            check_if_already_at_the_limit(data)
            fetch_data(data, data.current_page)
            choose_characters(data)
            take_character(data)
            determine_gender(data)
            write_to_csv(data)
        except NoMainCharactersError as error:
            print(error.message)
            continue
        except MaxPageExceededError as error:
            print(error.message)
            continue
        except MaleCharacterError as error:
            print(error.message)
            continue
        except DuplicateEntryError as error:
            print(error.message)
            continue
        except MaxCallsReachedError as error:
            print(error.message)
            break
        except NoMediaFoundError as error:
            print(error.message)
            break
        else:
            break
        finally:
            data.free_resources()

    # pprint.pprint(vars(data))


if __name__ == "__main__":
    main()
