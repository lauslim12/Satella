#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

def main():
    pass


if __name__ == "__main__":
    main()
