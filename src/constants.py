# Application
FILENAME = "data/suggestions.csv"
CSV_HEADER = [
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

# Genderize
GENDERIZE_API_URL = "https://api.genderize.io"

# AniList
ANILIST_API_URL = "https://graphql.anilist.co"
API_MAX_CALL_PER_PROGRAM = 25  # max is 90, but I'm not pushing my luck.
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
