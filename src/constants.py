"""This file will store all of the constants needed to operate the program."""

from os import path

# Application constants.
BIAS_PERCENTAGE = 85
FILENAME = "suggestions.csv"
FILENAME_PATH = path.abspath(path.join(path.dirname(__file__), "..", "data", FILENAME))
LOGGING_FILENAME = "satella-log.log"
LOGGING_PATH = path.abspath(path.join(path.dirname(__file__), "..", LOGGING_FILENAME))
CSV_HEADERS = [
    "character_id",
    "first_name",
    "last_name",
    "full_name",
    "favorites",
    "gender",
    "gender_probability",
    "anime_name",
    "date_taken",
]

# CLI purposes.
DESCRIPTION = """
Satella is a program that helps you get your favorite characters via a personalized algorithm. Contribute to the project by contacting @lauslim12 on GitHub!
"""
EPILOG = """
Please enjoy! If you have any issues or have any suggestions, please contact @lauslim12 on GitHub!
"""

# Genderize constants.
GENDERIZE_API_URL = "https://api.genderize.io"

# AniList constants.
ANILIST_API_URL = "https://graphql.anilist.co"
GRAPHQL_QUERY = """
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
"""
