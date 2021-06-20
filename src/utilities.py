"""Utility functions for the program."""

from argparse import ArgumentParser, Namespace
from csv import writer
from datetime import datetime
from math import ceil
from random import randint

from constants import (
    BIAS_PERCENTAGE,
    CSV_HEADERS,
    DESCRIPTION,
    EPILOG,
    FILENAME_PATH,
    LOGGING_PATH,
)


def clean_csv() -> None:
    """Purges and cleans the CSV, leaving headers only."""
    with open(FILENAME_PATH, "w", encoding="utf-8", newline="") as csv_file:
        csv_writer = writer(csv_file, delimiter=",")
        csv_writer.writerow(CSV_HEADERS)


def clean_logs() -> None:
    """Purges and cleans the log file."""
    with open(LOGGING_PATH, "w"):
        pass


def generate_weighted_random(max_pages: int) -> int:
    """Function to generate weighed random number using Inverse CDF method.
    The number generated will be biased towards upper numbers, ceiled.
    If the data is too small, we will not be using this function.
    Usually, that is because we queried by anime ID. Result is only 1 if that happens.
    """
    if max_pages == 1:
        return 1

    top_anime_pages = ceil(max_pages * 0.1)
    number = randint(1, 100)

    if number <= BIAS_PERCENTAGE:
        return randint(1, top_anime_pages)

    return randint(top_anime_pages + 1, max_pages)


def initialize_args() -> Namespace:
    """Initializes arguments for the program. Will be on a global scope."""
    parser = ArgumentParser(
        description=DESCRIPTION,
        epilog=EPILOG,
    )
    parser.add_argument(
        "-c",
        "--clean",
        help="Cleans the output CSV file except the header",
        action="store_true",
    )
    parser.add_argument(
        "-i",
        "--id",
        help="The anime ID that you want to query, disables the query by year",
        dest="specified_anime_id",
        type=int,
    )
    parser.add_argument(
        "-y",
        "--year",
        help="The year to search for the animes",
        dest="year",
        default=datetime.now().year,
        type=int,
    )
    parser.add_argument(
        "-s",
        "--season",
        help="The season to search for the animes. Combine with --year for better filtering",
        dest="season_name",
        choices=["SPRING", "SUMMER", "FALL", "WINTER"],
        type=str,
    )
    parser.add_argument(
        "-amc",
        "--allow-male-characters",
        help="To disable exception being thrown if the character found is a male character",
        dest="allow_male_characters",
        action="store_true",
    )
    parser.add_argument(
        "-anc",
        "--allow-none-characters",
        help="To disable exception being thrown if the character found is of unknown gender",
        dest="allow_none_characters",
        action="store_true",
    )

    args = parser.parse_args()

    return args
