# TODO: Combine to one script with 'main.py'
from csv import writer

# Constants
FILENAME = 'data/suggestions.csv'
HEADERS = ['character_id', 'first_name', 'last_name', 'full_name',
           'favorites', 'gender', 'gender_probability', 'anime_name', 'date_taken']


def clear_csv():
    with open(FILENAME, 'w', encoding='utf-8', newline='') as csv_file:
        csv_writer = writer(csv_file, delimiter=',')
        csv_writer.writerow(HEADERS)

    print("Data successfully cleaned! Enjoy using the application!")
    return None


def main():
    clear_csv()


if __name__ == "__main__":
    main()
