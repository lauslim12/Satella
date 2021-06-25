# Satella

Satella is a dedicated Windows / Linux tool to get a recommendation of seasonal / yearly characters (and in extension the animes that they are in) that you might like every day with a personalized algorithm. The source code has been rewritten in Python 3.9 and uses aiohttp to highly improve performance.

<p align="center">
  <img src="https://img.shields.io/badge/License-BSD--3--Revised-yellow"/>
  <img src="https://img.shields.io/badge/Coded%20with-Python-%233572A5"/>
</p>

## Introduction

Satella is a dedicated repository that helps you to get a recommendation of seasonal anime characters that you might like every day. Satella gathers data from [AniList GraphQL API](https://anilist.gitbook.io/anilist-apiv2-docs/) and will determine what gender they are by using [Genderize API](https://genderize.io/). How Satella gathers data depends on a multitude of factors, such as a specified year, number of times the anime that the character is in has been favorited, how popular is the anime, and the character role is taken into account. However, duplicate data is not allowed in this application, as it is highly redundant.

This application runs on Shell and Python, and mostly relies on crontabs to get it working automatically each day. Data gathered from Satella will be stored in a CSV file for further processing (further processing could be displaying it in a website, or even as simple as opening the CSV on a Microsoft Excel and inferring it by yourself).

It is recommended to run Satella on a low-power micro-computer such as Raspberry Pi Model A+. I personally use it and it makes the automation easier and less costly.

## Architecture

- Internet Of Things
- Asynchronous Programming
- Python Programming Language
- Shell Scripts and Micro Computers for Automation

## Philosophy

The name 'Satella' comes from the the character 'Satella' from Re:Zero. I actually like the name, so I named the repository after her.

## Requirements

In order to run the baseline of this application, you just need the following two things.

- Windows / Linux Environment (Linux is recommended)
- Python 3.9 and up
- Poetry (optional)

In order to automate the application, then you will also need these:

- Raspberry Pi (any version is fine, optional, you can use other micro computers)
- Raspbian OS (for the Raspberry Pi, also optional)

## How it Works

Satella works by following below steps (simplified):

1. First off, the program will check the maximum pages that is available on the API.

2. Then, Satella will fetch random data based on the GraphQL query on the `src/constants.py` file. One of the distinguishing features of Satella is that this program implements weighed random number generator in order to decide which data to be taken. The weighed number generator is 85% biased towards the number with higher favorites (means that you are more likely to get a character from a higher-favorited anime). As an added note, 'higher favorites' that we mean here is the top 10% anime for the current year. In other words, you are more likely to get a character from the top 10% anime of this year.

3. If you are querying by ID and there are no animes found, the program will immediately stop its execution.

4. If there is an anime, then the program will check whether it has supporting characters or not. If not, then the program will only take the main characters. If yes, then it is 50-50 chance to get either a main character or a supporting character. We will take the 'pool' or the array of main characters or the supporting characters.

5. If there is more than one page in the array of characters, we will then generate another random number (this time not a weighed random number), based on the available 'pages' that is available on the characters pool. If it only consists of one page, we will simply take one of the main characters or one of the supporting characters, as specified in step (4).

6. We make another randomized choice to take a character from the main characters pool (if in step (4) we had gotten a main character as our character to take from) or from the supporting characters pool (if in step (4) we had gotten a supporting character as our character to take from).

7. Make asynchronous API calls to the Genderize API (with the Japan country setting and the worldwide country setting) by sending our gained character name. If the gender of the character is the same as the configurations, we will take it to immediately. If the gender is invalid or not the same as the configurations, we will compare it with the result of the worldwide settings. If it is still invalid, we will restart from step (1).

8. Check if we have the same character (duplicate) in the CSV output file. If there is, start again from step (1).

9. We simply write the data of the character that we have already taken beforehand into a CSV file (`data/suggestions.csv` in this case).

All network requests are processed with aiohttp asynchronously for performance. Don't forget to remember to follow [AniList API Terms Of Use](https://anilist.gitbook.io/anilist-apiv2-docs/), and remember not to hoard large amounts of data! Use this tool with responsibility!

## Project Structure

The project structure itself is very simple.

- The `auto` folder is used to store the automation scripts.
- The `data` folder contains the output CSV file.
- The `src` folder contains the project files.
- There are also `.pylintrc`, `mypy.ini`, `poetry.lock`, `pyproject.toml` for Python dependency management.
- The rest are usual Git documents (`.gitignore`, `CONTRIBUTING.md`, `README.md`, `LICENSE`).

## Installation

The installation guide assumes that you are using Linux for this part. For those using Windows, you just have to replace the `python3` with `python`. For the automation, just use the `main.bat` (instead of `main.sh`) file. Personally, I use my Raspberry Pi via SSH to do the installation steps.

### General Setup

The following setup is used to start the application on its basic form.

- Ensure that your Python is 3.9 or up!

```bash
python3 --version
```

- First off, fork my repository, then clone it. I am going to assume that you cloned the repository to the `Home` directory.

```bash
git clone <YOUR_FORK_URL>
cd $HOME/Satella
```

- Second, create a Python Virtual Environment (in your Linux machine), install `poetry` as the package manager, and then install the dependencies. You can also use the `setup.py` if you wish for it. This setup is dedicated for **development** environment.

```bash
python3 -m venv .venv
source ".venv/bin/activate"
pip3 install poetry
poetry install
```

- Alternatively, you can install `poetry` with the recommended way.

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

- A note to keep in mind, if you just want to install the **production** environment (also known as plug-and-play), then you just need to install the production requirements.

```bash
poetry install --no-dev
```

- As an initial setup, clear all the data that I might have in my repository.

```bash
python3 src/main.py --clean
```

- Actually, after above steps are done, you can easily run the application using the following command. However, there is no automation yet, as we have not yet set it up.

```bash
python3 src/main.py <OPTIONAL_ARGUMENTS>
```

- The application will then run, and then it will store its results in the `data/suggestions.csv` file.

- As a note, optional arguments are explained in below setup.

### Automation Setup

This project is setup so that it could be automated everyday. I personally recommend you to use low-powered micro computers (also known as single board computers) like Raspberry Pi, BeagleBoard, Odroid, Banana Pi, and any other micro computers that you might have. The reason I recommended you those tools is because they are low-powered computers (electric bills are expensive nowadays) and they are literally equipped to be turned on 24/7 for IoT purposes. I use Raspberry Pi as it already had Git and Python installed the moment I installed the Raspbian OS.

- First, in order to automate the gathering of anime characters, you have to modify the `main.sh` file as you see fit with your own arguments. Below are the list of the arguments available for this program.

| Abbreviation |        Argument         |                                                                                     Purpose                                                                                      |   Default    |
| :----------: | :---------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :----------: |
|      -h      |         --help          |                                                                            Prints out the help screen                                                                            |     None     |
|      -c      |         --clean         |                                 Clears the CSV file with the exception of the header. The `--clean` parameter cannot be used with anything else!                                 |   `False`    |
|      -i      |          --id           |      Randomly selects a character from an anime based on its media ID (from AniList). Remember that you can't search by year or the season name if you use this parameter!       |     None     |
|      -y      |         --year          |                                                      Randomly selects a character from animes based on its year of release                                                       | Current year |
|      -s      |        --season         | Used to find a random character based on an anime from a season. Combine this with `--year` for better filtering. Options available are `WINTER`, `SPRING`, `SUMMER`, and `FALL` |     None     |
|     -amc     | --allow-male-characters |                                                    Used to disable exception being thrown if the character is of male gender                                                     |   `False`    |
|     -anc     | --allow-none-characters |                                                   Used to disable exception being thrown if the character is of unknown gender                                                   |   `False`    |

- Usage example from the `main.sh` file:

```bash
cd $HOME/Satella/auto
nano main.sh

# Modified line in the main.sh file.
python3 src/main.py --year 2020 -s FALL

# This works as well (chaining multiple arguments).
python3 src/main.py --year 2021 --season WINTER --allow-none-characters

# An another alternative is to search for characters from an anime based on its media ID.
python3 src/main.py --id 113813             # We are searching for characters from anime 'Kanojo, Okarishimasu'.

# Alternatives for the optional parameters.
python3 src/main.py --clean                 # Cleans the CSV file with the exception of the header.
python3 src/main.py --year 2019             # Get an anime from 2019.
python3 src/main.py --season SUMMER         # Get an anime from the summer season.
python3 src/main.py --allow-male-characters # Allows male characters.
```

- Do not forget to check the `PYTHON_VENV` variable. Is it the same as your Python Virtual Environment that you created beforehand? If no, change it to your virtual environment.

```bash
PYTHON_VENV=.venv # Replace this '.venv' with your virtual environment.
```

- Even if you did not set up your own custom arguments / filters, you can always just leave it be and it will be run with default arguments.

- After that, we need to setup our own crontab with Linux.

```bash
crontab -l
crontab -e
```

- You need the following script to be entered in your crontab. The following script is used to make automatic updates every 09:00 AM.

```bash
00 09 * * * cd "$HOME/Satella/auto" && bash main.sh
```

- As a precaution, you might need to set permissions for the repository folder.

```bash
sudo chmod -R 777 "$HOME/Satella"
```

- Do not forget to setup your Git account in your machine so you can make automated cronjobs everyday.

```bash
git config user.name <YOUR_USERNAME>
git config user.email <YOUR_EMAIL>
git config --list

# Then, create a random commit to authenticate your password.
# Next, check your remotes.
git remote -v                         # Check if the remote exists.
git remote add origin <YOUR_FORK_URL> # If the remote doesn't exist, then use your fork.
```

- Alternatively, you could use SSH in order to free yourself from the hassle of authenticating Git everyday. The guide to setup your own SSH with Linux can be [seen here (answer from StackOverflow)](https://stackoverflow.com/questions/8588768/how-do-i-avoid-the-specification-of-the-username-and-password-at-every-git-push). Make sure that you have already configured your `git config user.name` and `git config user.email`.

```bash
cd $HOME
ssh-keygen -t rsa -b 4096 -C <YOUR_GITHUB_EMAIL>
cd .ssh
ls -a             # Check out your RSA '.pub' name.
cat id_rsa.pub    # The default identifier is 'id_rsa'. You probably have a different identifier.

# Then, configure your access keys with your GitHub configuration. After that, test your connection.
ssh -T git@github.com
git remote set-url origin git+ssh://git@github.com/username/reponame.git # Replace with your fork URL!
```

- Enjoy your new anime character recommendation everyday! Just check your own repository for any new updates!

- To check if our crontab had run successfully:

```bash
sudo grep CRON /var/log/syslog
```

- You can also check the logs to check for the actions that the application has made.

```bash
cd $HOME/Satella
cat satella-log.log
```

- Note that if you are using Windows as your machine that will run this program, you could bind the `main.bat` script to Windows Task Scheduler. I believe you just need to follow the instructions from the GUI to setup the scheduled tasks.

## Data Inference

- The data can be opened using a spreadsheet application (Microsoft Excel or its open source counterpart) or read raw.

## Contribution

Satella is completely open source and contribution to this tool is highly encouraged for everyone! Please take a look at `CONTRIBUTING.md` file and enjoy contributing!

If you have found any issues during your usage of this program, please submit an issue and I'll go back to you right away.

## License

This application is licensed under BSD-3 License. Please see the `LICENSE` file for more information.

## Credits

I hereby offer thanks and credits to the following services and providers:

- [AniList.co](https://anilist.co/) for providing the GraphQL API.
- [Genderize.io](https://genderize.io/) for providing the API to predict the gender of a person based on their name.

Feel free to cite everything from this repository, as long as you give your credit. Satella is not related in any way, shape, or form to my work or my research. Satella is just a personal interest turned open source.
