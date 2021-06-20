"""This file will store all of the constants needed to operate the program."""

from os import path

# Application constants.
BIAS_PERCENTAGE = 85
FILENAME = "suggestions.csv"
FILENAME_PATH = path.abspath(path.join(path.dirname(__file__), "..", "data", FILENAME))
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
