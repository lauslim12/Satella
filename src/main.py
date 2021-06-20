"""Main functions, the application heart is located here."""

import asyncio
import logging
from csv import writer
from datetime import datetime
from random import choice, randint

from anilist import (
    all_main_characters,
    all_supporting_characters,
    anime_media,
    anime_page_info,
    fetch_from_anilist,
    fetch_from_anilist_specific_page,
    main_characters_page_info,
    supporting_characters_page_info,
)
from constants import FILENAME_PATH, LOGGING_PATH
from datatypes import (
    AniListRawResponse,
    Character,
    Data,
    GenderizeResponse,
    ProcessedData,
)
from exceptions import (
    DuplicateEntryError,
    InvalidCharacterGenderError,
    NoMainCharactersError,
    NoMediaFoundError,
)
from genderize import fetch_genders_from_genderize
from utilities import clean_csv, clean_logs, generate_weighted_random, initialize_args

# Global scope, the arguments passed.
args = initialize_args()


async def find_max_pages(year: int) -> int:
    """Finds the max pages for the current year."""
    response = await fetch_from_anilist({"year": year})
    total_page: int = anime_page_info(response)["total"]

    return total_page


async def fetch_anime_data(max_pages: int) -> AniListRawResponse:
    """Fetches the anime data according to the variables passed."""
    page_to_search = generate_weighted_random(max_pages)
    variables = {"year": args.year, "page": page_to_search}

    if args.specified_anime_id:
        variables = {"id": args.specified_anime_id}
    elif args.specified_anime_id is None and args.season_name:
        variables = {**variables, "seasonName": args.season_name}

    api_response = await fetch_from_anilist(variables)

    if not api_response["data"]["Page"]["media"]:
        raise NoMediaFoundError("There is no media with that identifier!")

    return api_response


async def get_character(api_response: AniListRawResponse) -> Data:
    """Gets a character from the API response."""
    anime_id = anime_media(api_response)["id"]
    anime_name = anime_media(api_response)["title"]["userPreferred"]
    main_pages = main_characters_page_info(api_response)["lastPage"]
    supporting_pages = supporting_characters_page_info(api_response)["lastPage"]
    main_characters = main_characters_page_info(api_response)["total"]
    supporting_characters = supporting_characters_page_info(api_response)["total"]

    # raise exception if no main characters are found.
    if main_characters == 0:
        raise NoMainCharactersError(f"There are no characters for anime: {anime_name}!")

    # if there are any supporting characters, make a choice.
    if supporting_characters > 0:
        take_from_main_characters = choice([True, False])
    else:
        take_from_main_characters = True

    # take data from main characters.
    if take_from_main_characters:
        page_to_take = randint(1, main_pages)

        if page_to_take > 1:
            response = await fetch_from_anilist_specific_page(anime_id, page_to_take)
            character = choice(all_main_characters(response))
            return {**character, "anime": anime_name}

        character = choice(all_main_characters(api_response))
        return {**character, "anime": anime_name}

    # take data from supporting characters.
    page_to_take = randint(1, supporting_pages)

    if page_to_take > 1:
        response = await fetch_from_anilist_specific_page(anime_id, page_to_take)
        character = choice(all_supporting_characters(response))
        return {**character, "anime": anime_name}

    character = choice(all_supporting_characters(api_response))
    return {**character, "anime": anime_name}


async def determine_gender(character: Data) -> list[GenderizeResponse]:
    """Determines the gender of the character."""
    character_name = character["name"]

    if character_name["first"]:
        character_name = character_name["first"].strip()
    else:
        character_name = character_name["last"].strip()

    genderize_parameters = [
        f"?name={character_name}&country_id=JP",
        f"?name={character_name}",
    ]

    result: list[GenderizeResponse] = await fetch_genders_from_genderize(
        genderize_parameters
    )
    return result


def get_essential_data(
    character: Character, gender: list[GenderizeResponse]
) -> ProcessedData:
    """Gets the essential data of the character to be written to the CSV file."""
    japanese_genderize = gender[0]
    worldwide_genderize = gender[1]

    # if allow both male/none characters
    if args.allow_male_characters and args.allow_none_characters:
        return {"character": character, "gender": japanese_genderize}

    # if allow male characters
    if args.allow_male_characters and (
        japanese_genderize["gender"] == "male"
        and japanese_genderize["probabilty"] > 0.50
    ):
        return {"character": character, "gender": japanese_genderize}

    if args.allow_male_characters and (
        worldwide_genderize["gender"] == "male"
        and worldwide_genderize["probability"] > 0.50
    ):
        return {"character": character, "gender": worldwide_genderize}

    # if only allow female characters
    if (
        japanese_genderize["gender"] == "female"
        and japanese_genderize["probability"] > 0.50
    ):
        return {"character": character, "gender": japanese_genderize}

    if (
        worldwide_genderize["gender"] == "female"
        and worldwide_genderize["probability"] > 0.50
    ):
        return {"character": character, "gender": worldwide_genderize}

    raise InvalidCharacterGenderError("Invalid character gender generated!")


def write_to_csv(processed_data: ProcessedData) -> None:
    """Writes the data to the CSV file."""
    character = processed_data["character"]
    gender = processed_data["gender"]

    # check for duplicates before inserting the data.
    with open(FILENAME_PATH, "r", encoding="utf-8") as csv_file:
        character_id = character["id"]
        if str(character_id) in csv_file.read():
            raise DuplicateEntryError(f"Character {character_id} already exists!")

    # write file to csv
    with open(FILENAME_PATH, "a", newline="", encoding="utf-8") as csv_file:
        csv_writer = writer(csv_file)
        csv_writer.writerow(
            [
                character["id"],
                character["name"]["first"],
                character["name"]["last"],
                character["name"]["full"],
                character["favourites"],
                gender["gender"],
                gender["probability"],
                character["anime"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ]
        )


async def main() -> None:
    """Driver code to run the program."""
    # initialize logging to analyze errors
    logging.basicConfig(filename=LOGGING_PATH, level=logging.INFO)

    # if argument 'clean' is here, purge csv and logs
    if args.clean:
        clean_csv()
        clean_logs()
        return

    # enter main asynchronous loop
    while True:
        try:
            max_pages = await find_max_pages(args.year)
            api_data = await fetch_anime_data(max_pages)
            character = await get_character(api_data)
            gender = await determine_gender(character)
            processed_data = get_essential_data(character, gender)
            print(processed_data)
            # write_to_csv(processed_data)
        except (InvalidCharacterGenderError, NoMainCharactersError) as err:
            logging.info(err)
            continue
        except NoMediaFoundError as err:
            logging.info(err)
            break
        else:
            break


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_until_complete(asyncio.sleep(0))
    loop.close()
